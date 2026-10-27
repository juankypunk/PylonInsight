"""Integration test for BMU history measurement deduplication."""

import logging
from datetime import datetime
from uuid import uuid4

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.database.repositories.history_bmu import HistoryBMURepository
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device
from pyloninsight.models.history import History


def make_history(
    timestamp: datetime,
    *,
    module_voltage: int = 52000,
    module_temperature: int = 25,
) -> History:
    """Create a representative BMU history measurement."""
    return History(
        timestamp=timestamp,
        values={
            "module_voltage": module_voltage,
            "module_temperature": module_temperature,
            "temperature_low": 23,
            "temperature_high": 28,
            "cell_voltage_low": 3450,
            "cell_voltage_high": 3500,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "",
            "battery_events": "",
        },
    )


def get_module_voltage(connection, history_id: int) -> int:
    """Return the stored module voltage for a history measurement."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT module_voltage_mv
            FROM history_bmu
            WHERE id = %s
            """,
            (history_id,),
        )
        row = cursor.fetchone()

    assert row is not None, f"History measurement {history_id} was not found."
    return row[0]


def main() -> None:
    """Run integration checks against the configured PostgreSQL database."""
    connection = connect(DatabaseConfig.from_environment())

    token = uuid4().hex
    timestamp = datetime(2026, 7, 13, 20, 0, 0)
    campaign_ids = []

    try:
        campaign_repository = CampaignRepository(connection)
        device_repository = DeviceRepository(connection)
        export_repository = CampaignExportRepository(connection)
        history_repository = HistoryBMURepository(connection)

        # Create a test BMU device.
        device_id = device_repository.create(
            Device(
                barcode=f"TEST-HISTORY-BMU-{token}",
                device_type="BMU",
                manufacturer="Test",
                model="H48050",
            )
        )

        # Create two campaigns so the same physical measurement can
        # be associated with exports from different campaigns.
        first_campaign_id = campaign_repository.create(
            Campaign(
                name=f"test-history-bmu-first-{token}",
                description="Temporary BMU history integration test",
            )
        )
        campaign_ids.append(first_campaign_id)

        second_campaign_id = campaign_repository.create(
            Campaign(
                name=f"test-history-bmu-second-{token}",
                description="Temporary BMU history integration test",
            )
        )
        campaign_ids.append(second_campaign_id)

        first_export_id = export_repository.create(
            campaign_id=first_campaign_id,
            device_id=device_id,
            campaign_export=CampaignExport(
                role="BMU1",
                export_timestamp=datetime(2026, 7, 13, 20, 5, 0),
            ),
        )

        second_export_id = export_repository.create(
            campaign_id=second_campaign_id,
            device_id=device_id,
            campaign_export=CampaignExport(
                role="BMU1",
                export_timestamp=datetime(2026, 7, 13, 20, 6, 0),
            ),
        )

        original_record = make_history(timestamp)

        # 1. A new measurement should be inserted.
        first_result = history_repository.create_many(
            device_id=device_id,
            campaign_export_id=first_export_id,
            records=[original_record],
        )

        assert len(first_result) == 1
        history_id = first_result[0]
        assert get_module_voltage(connection, history_id) == 52000

        print("New measurement insertion verified.")

        # 2. The same measurement in another export should reuse
        #    the existing database row.
        second_result = history_repository.create_many(
            device_id=device_id,
            campaign_export_id=second_export_id,
            records=[original_record],
        )

        assert second_result == [history_id]

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM history_bmu
                WHERE device_id = %s
                  AND record_timestamp = %s
                """,
                (device_id, timestamp),
            )
            assert cursor.fetchone() == (1,)

        print("Measurement reuse across exports verified.")

        # 3. Repeating the measurement for the same export must not
        #    create a duplicate association.
        repeated_result = history_repository.create_many(
            device_id=device_id,
            campaign_export_id=second_export_id,
            records=[original_record],
        )

        assert repeated_result == [history_id]

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM history_bmu_export
                WHERE history_bmu_id = %s
                  AND campaign_export_id = %s
                """,
                (history_id, second_export_id),
            )
            assert cursor.fetchone() == (1,)

        print("Duplicate association prevention verified.")

        # 4. Conflicting values for the same device and timestamp must
        #    not overwrite the measurement already stored.
        conflicting_record = make_history(
            timestamp,
            module_voltage=53000,
        )

        warning_capture = logging.Handler()
        warning_capture.messages = []

        def capture_warning(record: logging.LogRecord) -> None:
            warning_capture.messages.append(record.getMessage())

        warning_capture.emit = capture_warning

        logger = logging.getLogger("pyloninsight.database.repositories.history_bmu")
        logger.addHandler(warning_capture)
        logger.setLevel(min(logger.level or logging.WARNING, logging.WARNING))

        try:
            conflicting_result = history_repository.create_many(
                device_id=device_id,
                campaign_export_id=first_export_id,
                records=[conflicting_record],
            )
        finally:
            logger.removeHandler(warning_capture)

        assert conflicting_result == [history_id]

        # Verify that the original value remains unchanged.
        assert get_module_voltage(connection, history_id) == 52000

        assert any(
            "Conflicting BMU history values" in message
            for message in warning_capture.messages
        ), "Expected a warning about conflicting BMU history values."

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM history_bmu
                WHERE device_id = %s
                  AND record_timestamp = %s
                """,
                (device_id, timestamp),
            )
            assert cursor.fetchone() == (1,)

        print("Conflicting values preserve the original measurement.")
        print("Conflict warning verified.")
        print("BMU history integration test PASSED.")

    finally:
        # All test operations are intentionally left uncommitted.
        # Rolling back removes the temporary campaigns, exports,
        # device and history measurements, even if an assertion fails.
        try:
            connection.rollback()
        finally:
            connection.close()


if __name__ == "__main__":
    main()
