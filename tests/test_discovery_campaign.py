from datetime import datetime
from pathlib import Path

from pyloninsight.discovery import discover_campaign
from pyloninsight.parsers.detailed import parse_detailed

REAL_CAMPAIGN = Path("tests/data/real/2026-07-13_SOC100")


def test_discover_campaign_capture_date():
    campaign = discover_campaign(REAL_CAMPAIGN)

    assert campaign.capture_date == datetime(2026, 7, 13, 20, 19, 30)


def test_discover_campaign_export_timestamps():
    campaign = discover_campaign(REAL_CAMPAIGN)

    # for export in campaign.exports:
    #    print(export.role, "->", export.export_timestamp)

    timestamps = {export.role: export.export_timestamp for export in campaign.exports}

    assert timestamps["BMS"] == datetime(2026, 7, 13, 20, 19, 30)
    # completar BMU1/BMU2/BMU3 con los timestamps reales
    assert timestamps["BMU1"] == datetime(2026, 7, 13, 20, 30, 51)
    assert timestamps["BMU2"] == datetime(2026, 7, 13, 20, 33, 46)
    assert timestamps["BMU3"] == datetime(2026, 7, 13, 20, 37, 32)
