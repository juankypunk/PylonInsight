from datetime import datetime
from uuid import uuid4

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.database.repositories.event_bmu import EventBMURepository
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device
from pyloninsight.models.event import Event


def make_event(item: int, event_code: str) -> Event:
    """Create a representative legacy BMU event."""

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
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "Normal",
            "battery_events": event_code,
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
        event_repository = EventBMURepository(connection)

        campaign_id = campaign_repository.create(
            Campaign(
                name=f"test-event-bmu-{uuid4()}",
                description="Temporary EventBMURepository integration test",
            )
        )
        print(f"Created campaign: {campaign_id}")

        device_id = device_repository.create(
            Device(
                barcode=f"TEST-BMU-{uuid4()}",
                device_type="BMU",
                manufacturer="Test",
                model="H48050",
            )
        )
        print(f"Created device: {device_id}")

        export_id = export_repository.create(
            campaign_id=campaign_id,
            device_id=device_id,
            campaign_export=CampaignExport(
                role="BMU1",
                export_timestamp=datetime(2026, 7, 13, 20, 30),
                events=[
                    make_event(1, "BHV"),
                    make_event(2, "BLV"),
                ],
            ),
        )
        print(f"Created campaign export: {export_id}")

        inserted_ids = event_repository.create_many(
            campaign_export_id=export_id,
            events=[
                make_event(1, "BHV"),
                make_event(2, "BLV"),
            ],
        )
        print(f"Inserted event IDs: {inserted_ids}")

        assert len(inserted_ids) == 2

        first = event_repository.get_by_id(inserted_ids[0])
        second = event_repository.get_by_id(inserted_ids[1])

        assert first is not None
        assert first.item == 1
        assert first.event_code == "BHV"
        assert first.values["module_voltage"] == 52000
        assert first.values["module_temperature"] == 25
        assert first.values["events"] == "Normal"
        assert first.values["battery_events"] == "BHV"

        assert second is not None
        assert second.item == 2
        assert second.event_code == "BLV"
        assert second.values["battery_events"] == "BLV"

        print("Event BMU insertion and retrieval OK")

    finally:
        try:
            # A failed SQL statement can leave the transaction aborted.
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
