from pathlib import Path

from pyloninsight.parsers.detailed import parse_detailed

REAL_CAMPAIGN = Path(__file__).parent / "data" / "real" / "2026-07-13_SOC100"


def detailed_file(role: str) -> Path:
    files = list((REAL_CAMPAIGN / role / "history").glob("*_detailed.txt"))

    assert len(files) == 1

    return files[0]


def test_parse_real_bms() -> None:
    device, snapshot = parse_detailed(detailed_file("BMS"))

    assert device.barcode == "H220829100140097"
    assert device.manufacturer == "Pylon"
    assert device.model == "CMU_A"

    assert snapshot.board_version == "TISP01V10R02_1"
    assert snapshot.hardware_version == "V10R9C5"
    assert snapshot.firmware_version == "V5.7"
    assert snapshot.boot_version == "V1.4"
    assert snapshot.cell_count == 45
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 144.0

    assert snapshot.additional is not None
    assert snapshot.additional["main_soft_version"] == "B52.36.0"
    assert snapshot.additional["device_test_time"] == "2022-08-30 15:10:18"


def test_parse_real_legacy_bmu() -> None:
    device, snapshot = parse_detailed(detailed_file("BMU1"))

    assert device.barcode == "P224009002250028"
    assert device.manufacturer == "Pylon"
    assert device.model == "bmu"

    assert snapshot.board_version == "HP0115SV10R01"
    assert snapshot.firmware_version == "V3.2"
    assert snapshot.boot_version == "V1.4"
    assert snapshot.cell_count == 15
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 48.0

    assert snapshot.additional is not None
    assert snapshot.additional["main_soft_version"] == "B52.2.0"
    assert snapshot.additional["device_test_time"] == "2022-06-04 14:12:52"


def test_parse_real_xhb_bmu() -> None:
    device, snapshot = parse_detailed(detailed_file("BMU2"))

    assert device.barcode == "Y251113600040138"
    assert device.manufacturer == "Pylon"
    assert device.model == "XHB_BMU_NT"

    assert snapshot.board_version == "V30R02C002"
    assert snapshot.firmware_version == "V1.2"
    assert snapshot.boot_version == "V1.0"
    assert snapshot.cell_count == 15
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 48.0

    assert snapshot.additional is not None
    assert snapshot.additional["main_soft_version"] == "B52.5.0"
    assert snapshot.additional["device_test_time"] == "2025-11-20 09:09:31"
    assert snapshot.additional["fan_exist"] == "NO"
    assert snapshot.additional["module_afetype"] == "LTC6813"
