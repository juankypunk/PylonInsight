from datetime import datetime
from uuid import uuid4

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.database.repositories.event_xhb_bmu import (
    EventXHBMURepository,
)
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device
from pyloninsight.models.event import Event


def make_event(item: int, event_code: str) -> Event:
    """Create a representative XHB BMU event."""

    is_error = event_code == "SYSERR"

    return Event(
        item=item,
        timestamp=datetime(2026, 7, 13, 20, 19, item),
        event_code=event_code,
        values={
            "module_voltage": 52000,
            "module_temperature": 25,
            "temperature_low": 24,
            "temperature_high": 27,
            "cell_voltage_low": 3450,
            "cell_voltage_high": 3500,
            "positive_terminal_temperature": 26,
            "negative_terminal_temperature": 27,
            "reference_voltage": 3000,
            "fan_pwm": 50 if is_error else 0,
            "fan1_rpm": 1200 if is_error else 0,
            "fan2_rpm": 1180 if is_error else 0,
            "base_state": "SysError" if is_error else "Normal",
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "positive_terminal_temperature_state": "Normal",
            "negative_terminal_temperature_state": "Normal",
            "error_code": "0x20" if is_error else "0x00",
            "events": event_code,
        },
    )


def main():
    connection = connect(DatabaseConfig.from_environment())

    campaign_id = None
    device_id = None
    export_id = None

    try:
        campaign_repository = CampaignRepository(connection)
        device_repository = DeviceRepository(connection)
        export_repository = CampaignExportRepository(connection)
        event_repository = EventXHBMURepository(connection)

        campaign_id = campaign_repository.create(
            Campaign(
                name=f"test-event-xhb-bmu-{uuid4()}",
                description=("Temporary EventXHBMURepository integration test"),
            )
        )
        print(f"Created campaign: {campaign_id}")

        device_id = device_repository.create(
            Device(
                barcode=f"TEST-XHB-BMU-{uuid4()}",
                device_type="XHB_BMU",
                manufacturer="Test",
                model="XHB BMU NT",
            )
        )
        print(f"Created device: {device_id}")

        export_id = export_repository.create(
            campaign_id=campaign_id,
            device_id=device_id,
            campaign_export=CampaignExport(
                role="BMU2",
                export_timestamp=datetime(2026, 7, 13, 20, 30),
                events=[
                    make_event(1, "SYSERR"),
                    make_event(2, "Normal"),
                ],
            ),
        )
        print(f"Created campaign export: {export_id}")

        inserted_ids = event_repository.create_many(
            campaign_export_id=export_id,
            events=[
                make_event(1, "SYSERR"),
                make_event(2, "Normal"),
            ],
        )
        print(f"Inserted event IDs: {inserted_ids}")

        assert len(inserted_ids) == 2

        first = event_repository.get_by_id(inserted_ids[0])
        second = event_repository.get_by_id(inserted_ids[1])

        assert first is not None
        assert first.item == 1
        assert first.event_code == "SYSERR"
        assert first.values["module_voltage"] == 52000
        assert first.values["module_temperature"] == 25
        assert first.values["base_state"] == "SysError"
        assert first.values["error_code"] == "0x20"
        assert first.values["events"] == "SYSERR"
        assert first.values["fan1_rpm"] == 1200
        assert first.values["fan2_rpm"] == 1180

        assert second is not None
        assert second.item == 2
        assert second.event_code == "Normal"
        assert second.values["base_state"] == "Normal"
        assert second.values["error_code"] == "0x00"
        assert second.values["fan1_rpm"] == 0
        assert second.values["fan2_rpm"] == 0

        print("Event XHB BMU insertion and retrieval OK")

    finally:
        try:
            connection.rollback()

            if export_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM campaign_export WHERE id = %s",
                        (export_id,),
                    )
                connection.commit()

            if campaign_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM campaign WHERE id = %s",
                        (campaign_id,),
                    )
                connection.commit()

            if device_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM device WHERE id = %s",
                        (device_id,),
                    )
                connection.commit()
                print(f"Deleted temporary device: {device_id}")

        finally:
            connection.close()


if __name__ == "__main__":
    main()
