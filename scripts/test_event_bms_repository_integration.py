from datetime import datetime
from uuid import uuid4

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.database.repositories.event_bms import EventBMSRepository
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device
from pyloninsight.models.event import Event


def make_event(item: int, event_code: str) -> Event:
    return Event(
        item=item,
        timestamp=datetime(2026, 7, 13, 20, 19, item),
        event_code=event_code,
        values={
            "stack_voltage": 52000,
            "stack_current": 1200,
            "temperature": 25,
            "battery_temp_low": 24,
            "battery_temp_high": 27,
            "battery_voltage_low": 3450,
            "battery_voltage_high": 3500,
            "unit_temp_low": 23,
            "unit_temp_high": 28,
            "unit_voltage_low": 3440,
            "unit_voltage_high": 3510,
            "base_state": "Normal",
            "voltage_state": "Normal",
            "current_state": "Normal",
            "temperature_state": "Normal",
            "state_of_charge": 97,
            "error_code": "0x00",
            "events": event_code,
            "battery_events": "",
            "unit_events": "",
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
        event_repository = EventBMSRepository(connection)

        campaign_id = campaign_repository.create(
            Campaign(
                name=f"test-event-bms-{uuid4()}",
                description="Temporary EventBMSRepository integration test",
            )
        )
        print(f"Created campaign: {campaign_id}")

        device_id = device_repository.create(
            Device(
                barcode=f"TEST-BMS-{uuid4()}",
                device_type="BMS",
                manufacturer="Test",
                model="SC0500A",
            )
        )
        print(f"Created device: {device_id}")

        export_id = export_repository.create(
            campaign_id=campaign_id,
            device_id=device_id,
            campaign_export=CampaignExport(
                role="BMS",
                export_timestamp=datetime(2026, 7, 13, 20, 30),
                events=[make_event(1, "BHV"), make_event(2, "BLV")],
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
        assert first.values["stack_voltage"] == 52000
        assert first.values["state_of_charge"] == 97

        assert second is not None
        assert second.item == 2
        assert second.event_code == "BLV"

        print("Event BMS insertion and retrieval OK")

    finally:
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

        connection.close()


if __name__ == "__main__":
    main()
