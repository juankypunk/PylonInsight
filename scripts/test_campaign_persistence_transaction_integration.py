"""Integration test for transactional campaign persistence."""

from datetime import datetime
from uuid import uuid4

import psycopg

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.persistence import CampaignPersistence
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device


def main() -> None:
    config = DatabaseConfig.from_environment()
    token = uuid4().hex

    campaign_name = f"test-transaction-{token}"
    barcodes = [
        f"TEST-TX-{token[:28]}-1",
        f"TEST-TX-{token[:28]}-2",
    ]

    campaign = Campaign(
        name=campaign_name,
        description="Temporary transactional integration test",
    )

    for index, barcode in enumerate(barcodes):
        campaign.add_export(
            CampaignExport(
                role="BMS" if index == 0 else "INVALID_ROLE",
                export_timestamp=datetime.now(),
                device=Device(
                    barcode=barcode,
                    device_type="BMS",
                    manufacturer="Test",
                    model="SC0500A",
                ),
            )
        )

    connection = connect(config)
    verification_connection = connect(config)

    try:
        persistence = CampaignPersistence(connection)

        try:
            persistence.save(campaign)
        except psycopg.errors.InvalidTextRepresentation:
            print("Expected invalid enum value error received.")
        else:
            raise AssertionError(
                "Expected InvalidTextRepresentation for an invalid campaign role."
            )

        with verification_connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM campaign WHERE name = %s",
                (campaign_name,),
            )
            campaign_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM device WHERE barcode = ANY(%s)",
                (barcodes,),
            )
            device_count = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM campaign_export ce
                JOIN campaign c ON c.id = ce.campaign_id
                WHERE c.name = %s
                """,
                (campaign_name,),
            )
            export_count = cursor.fetchone()[0]

        assert (
            campaign_count == 0
        ), f"Campaign was not rolled back: {campaign_count} row(s) remain."
        assert (
            device_count == 0
        ), f"Device insertion was not rolled back: {device_count} row(s) remain."
        assert (
            export_count == 0
        ), f"Export insertion was not rolled back: {export_count} row(s) remain."

        print("Campaign rollback verified.")
        print("Device rollback verified.")
        print("Export rollback verified.")
        print("Transactional integration test PASSED.")

    finally:
        connection.close()
        verification_connection.close()


if __name__ == "__main__":
    main()
