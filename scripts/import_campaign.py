from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from pyloninsight.database.connection import DatabaseConfig, connect
from pyloninsight.database.persistence import CampaignPersistence
from pyloninsight.loader import load_campaign


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a BatteryView campaign into the PylonInsight database."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the campaign directory.",
    )
    return parser.parse_args()


def print_campaign_summary(campaign) -> None:
    print(f"\nCampaign: {campaign.name}")
    print(f"Capture date: {campaign.capture_date}")
    print(f"Exports: {len(campaign.exports)}")

    total_history = 0
    total_events = 0

    for export in campaign.exports:
        device = export.device

        print(f"\nRole: {export.role}")
        print(f"  Export timestamp: {export.export_timestamp}")

        if device is not None:
            print(f"  Model: {device.model}")
            print(f"  Barcode: {device.barcode}")

        print(f"  Snapshot: {'yes' if export.snapshot else 'no'}")
        print(f"  History records: {len(export.history)}")
        print(f"  Event records: {len(export.events)}")

        total_history += len(export.history)
        total_events += len(export.events)

    print(f"\nTOTAL history records: {total_history}")
    print(f"TOTAL event records: {total_events}")
    print(f"TOTAL records: {total_history + total_events}")


def campaign_exists(connection, campaign_name: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM campaign WHERE name = %s)",
            (campaign_name,),
        )
        return cursor.fetchone()[0]


def main() -> int:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    args = parse_args()

    try:
        campaign = load_campaign(args.path)
    except Exception as exc:
        print(f"Error loading campaign: {exc}", file=sys.stderr)
        return 1

    print_campaign_summary(campaign)

    try:
        config = DatabaseConfig.from_environment()
        with connect(config) as connection:
            if campaign_exists(connection, campaign.name):
                print(f"\nCampaign '{campaign.name}' already exists. Import cancelled.")
                return 1

            answer = (
                input("\nPersist this campaign to the database? [y/N]: ")
                .strip()
                .lower()
            )

            if answer not in {"y", "yes"}:
                print("Import cancelled.")
                return 0

            campaign_id = CampaignPersistence(connection).save(campaign)

        print(f"\nCampaign imported successfully. Database ID: {campaign_id}")
        return 0

    except Exception as exc:
        print(f"Error importing campaign: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
