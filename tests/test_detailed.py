from pathlib import Path

from pyloninsight.parsers.detailed import parse_detailed


def write_detailed(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "detailed.txt"
    path.write_text(content, encoding="utf-16-le")
    return path


def test_parse_legacy_bmu(tmp_path: Path) -> None:
    path = write_detailed(
        tmp_path,
        """\
info
@
Device address      : 1
Manufacturer        : Pylon
Device name         : bmu
Board version       : HP0115SV10R01
Main Soft version   : B52.2.0
Soft  version       : V3.2
Sub Soft version    : T1.0
Boot  version       : V1.4
Comm version        : V2.0
Release Date        : 21-09-29

Barcode             :
PCBA Barcode        : H1004005222T2202380714
Module Barcode      : P224009002250028
PowerSupply Barcode : ????????????????????????????????

Device Test Time    : 2022-06-04 14:12:52

Specification       : 48V/50AH
Cell Number         : 15
Command completed successfully
$$
pylon_debug>
stat
@
Data Items      :     2047
""",
    )

    device, snapshot = parse_detailed(path)

    assert device.barcode == "P224009002250028"
    assert device.manufacturer == "Pylon"
    assert device.model == "bmu"

    assert snapshot.board_version == "HP0115SV10R01"
    assert snapshot.hardware_version is None
    assert snapshot.firmware_version == "V3.2"
    assert snapshot.boot_version == "V1.4"
    assert snapshot.release_date is not None
    assert snapshot.release_date.isoformat() == "2021-09-29"
    assert snapshot.cell_count == 15
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 48.0

    assert snapshot.additional is not None
    assert snapshot.additional["main_soft_version"] == "B52.2.0"
    assert snapshot.additional["device_test_time"] == "2022-06-04 14:12:52"
    assert snapshot.additional["device_address"] == "1"


def test_parse_xhb_bmu(tmp_path: Path) -> None:
    path = write_detailed(
        tmp_path,
        """\
info
@
Device address           : 2
Manufacturer             : Pylon
Device name              : XHB_BMU_NT
Board version            : V30R02C002
Main Soft version        : B52.5.0
Soft  version             : V1.2
Boot  version            : V1.0
Comm version             : V2.0
Release Date             : 25-10-20
Module Barcode           : Y251113600040138
PCBA Barcode             : H300200225A18545700124
Specification            : 48V/50AH
Cell Number              : 15
Fan Exist                : NO
XHB_V3 Board             : NO
Module AfeType            : LTC6813
Module cellType          : 1
Device Test Time         : 2025-11-20 09:09:31

Command completed successfully
$$
pylon_debug>
stat
@
Data Items      :      182
""",
    )

    device, snapshot = parse_detailed(path)

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


def test_parse_bms(tmp_path: Path) -> None:
    path = write_detailed(
        tmp_path,
        """\
info
@
Device address      : 0
Manufacturer        : Pylon
Device name         : CMU_A
Board version       : TISP01V10R02_1
Hard  version       : V10R9C5
Main Soft version   : B52.36.0
Soft  version       : V5.7
Boot  version       : V1.4
Comm version        : V2.0
Release Date        : 23-08-25

Barcode             :
PCBA Barcode        : H100900522808750200398
Module Barcode      : H220829100140097
PowerSupply Barcode : H200100622805760300092

Device Test Time    : 2022-08-30 15:10:18

Specification       : 144V/50AH
Cell Number         : 45
Max Dischg Curr     : -55000mA
Max Charge Curr     : 53000mA
Shut Circuit        : Yes
Relay Feedback      : Yes
New Board           : Yes

Command completed successfully
$$
pylon_debug>
stat
@
EvenData Items      : 384
""",
    )

    device, snapshot = parse_detailed(path)

    assert device.barcode == "H220829100140097"
    assert device.manufacturer == "Pylon"
    assert device.model == "CMU_A"

    assert snapshot.board_version == "TISP01V10R02_1"
    assert snapshot.hardware_version == "V10R9C5"
    assert snapshot.firmware_version == "V5.7"
    assert snapshot.boot_version == "V1.4"
    assert snapshot.release_date is not None
    assert snapshot.release_date.isoformat() == "2023-08-25"
    assert snapshot.cell_count == 45
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 144.0

    assert snapshot.additional is not None
    assert snapshot.additional["main_soft_version"] == "B52.36.0"
    assert snapshot.additional["device_test_time"] == "2022-08-30 15:10:18"
    assert snapshot.additional["max_dischg_curr"] == "-55000mA"
