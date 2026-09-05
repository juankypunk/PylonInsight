from pathlib import Path

from pyloninsight.loader import load_campaign

REAL_CAMPAIGN = Path(__file__).parent / "data" / "real" / "2026-07-13_SOC100"


def get_export(campaign, role: str):
    for export in campaign.exports:
        if export.role.upper() == role.upper():
            return export

    raise AssertionError(f"Export not found: {role}")


def test_load_real_campaign_device_metadata() -> None:
    campaign = load_campaign(REAL_CAMPAIGN)

    assert campaign.name == "2026-07-13_SOC100"

    assert len(campaign.exports) == 4

    bms = get_export(campaign, "BMS")
    bmu1 = get_export(campaign, "BMU1")
    bmu2 = get_export(campaign, "BMU2")
    bmu3 = get_export(campaign, "BMU3")

    assert bms.device is not None
    assert bms.snapshot is not None

    assert bmu1.device is not None
    assert bmu1.snapshot is not None

    assert bmu2.device is not None
    assert bmu2.snapshot is not None

    assert bmu3.device is not None
    assert bmu3.snapshot is not None

    assert bms.device.model == "CMU_A"

    assert bmu1.device.model == "bmu"
    assert bmu3.device.model == "bmu"

    assert bmu2.device.model == "XHB_BMU_NT"


def test_load_real_campaign_identifies_legacy_and_xhb_modules() -> None:
    campaign = load_campaign(REAL_CAMPAIGN)

    bmu1 = get_export(campaign, "BMU1")
    bmu2 = get_export(campaign, "BMU2")
    bmu3 = get_export(campaign, "BMU3")

    assert bmu1.device is not None
    assert bmu2.device is not None
    assert bmu3.device is not None

    assert bmu1.device.model == "bmu"
    assert bmu2.device.model == "XHB_BMU_NT"
    assert bmu3.device.model == "bmu"

    assert bmu1.snapshot is not None
    assert bmu2.snapshot is not None
    assert bmu3.snapshot is not None

    assert bmu1.snapshot.board_version == "HP0115SV10R01"
    assert bmu2.snapshot.board_version == "V30R02C002"
    assert bmu3.snapshot.board_version == "HP0115SV10R01"
