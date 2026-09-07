from pathlib import Path

from datetime import datetime

from pyloninsight.loader import load_campaign


def write_detailed(path: Path, device_name: str = "bmu") -> None:
    path.write_text(
        f"""\
info
@
Device address      : 1
Manufacturer        : Pylon
Device name         : {device_name}
Board version       : HP0115SV10R01
Main Soft version   : B52.2.0
Soft  version       : V3.2
Sub Soft version    : T1.0
Boot  version       : V1.4
Comm version        : V2.0
Release Date        : 21-09-29
Module Barcode      : P224009002250028
PCBA Barcode        : H1004005222T2202380714
Device Test Time    : 2022-06-04 14:12:52
Specification       : 48V/50AH
Cell Number         : 15
Command completed successfully
$$
pylon_debug>
stat
@
Data Items          : 2047
""",
        encoding="utf-16-le",
    )


def write_bmu_history(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Header
Header
1,26-07-13,12:00:00,48000,25,24,26,3300,3310,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def create_minimal_export(device_path: Path) -> None:
    history_dir = device_path / "history"
    events_dir = device_path / "events"

    history_dir.mkdir(parents=True)
    events_dir.mkdir(parents=True)

    write_bmu_history(history_dir / "UnknownSN_history.csv")

    (events_dir / "UnknownSN_event.csv").write_text(
        "",
        encoding="utf-8",
    )


def write_bms_history(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Header
Item,Time,Vo(mV),Cu(mA),Tempr,BTlow,BThigh,BVlow,BVhigh,UTlow,UThigh,UVlow,UVhigh,Base.St,Volt.St,Curr.St,Temp.St,Per%,ErrCode,Events,BatEvents,UnitEvents
1,26-07-13,12:00:00,48000,1000,25,24,26,48000,48100,25,26,47900,48000,0,0,0,0,100%,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def write_xhb_bmu_history(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Header
Header
1,26-07-13,12:00:00,48000,25,24,26,48000,48100,25,26,3300,3400,5000,50,1000,1100,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def write_xhb_bmu_history_for_events(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Header
Item,Date,Time,Vo(mV),Tmpr,BTlow,BThigh,BVlow,BVhigh,PT.Tmpr,NT.Tmpr,Ref.Vol,Fan.Pwm,Fan1.Rpm,Fan2.Rpm,Base.St,Volt.St,Tmpr.St,PT.Tmpr.St,NT.Tmpr.St,Err.Code,Events
1,26-07-13,12:00:00,48000,25,24,26,3300,3400,5000,50,1000,1100,1200,1300,0,0,0,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def write_bmu_events(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Item,Date,Time,Vo(mV),Tempr,Tlow,Thigh,Vlowest,Vhighest,Volt.St,Temp.St,Events,BatEvents
1,26-07-13,12:00:00,48000,25,24,26,3300,3310,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def write_xhb_bmu_events(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Item,Date,Time,Vo(mV),Tmpr,BTlow,BThigh,BVlow,BVhigh,PT.Tmpr,NT.Tmpr,Ref.Vol,Fan.Pwm,Fan1.Rpm,Fan2.Rpm,Base.St,Volt.St,Tmpr.St,PT.Tmpr.St,NT.Tmpr.St,Err.Code,Events
1,26-07-13,12:00:00,48000,25,24,26,3300,3400,5000,50,1000,1100,1200,1300,0,0,0,0,0,0,123
Command completed successfully
""",
        encoding="utf-8",
    )


def write_bms_events(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Item,Date,Time,Vo(mV),Cu(mA),Tempr,BTlow,BThigh,BVlow,BVhigh,UTlow,UThigh,UVlow,UVhigh,Base.St,Volt.St,Curr.St,Temp.St,Per%,ErrCode,Events,BatEvents,UnitEvents
1,26-07-13,12:00:00,48000,1000,25,24,26,48000,48100,25,26,47900,48000,0,0,0,0,100%,0,123,456,789
Command completed successfully
""",
        encoding="utf-8",
    )


def write_bms_history_for_events(path: Path) -> None:
    path.write_text(
        """\
Header
Header
Item,Date,Time,Vo(mV),Cu(mA),Tempr,BTlow,BThigh,BVlow,BVhigh,UTlow,UThigh,UVlow,UVhigh,Base.St,Volt.St,Curr.St,Temp.St,Per%,ErrCode,Events,BatEvents,UnitEvents
1,26-07-13,12:00:00,48000,1000,25,24,26,48000,48100,25,26,47900,48000,0,0,0,0,100%,0,0,0,0
Command completed successfully
""",
        encoding="utf-8",
    )


def test_load_campaign_loads_device_metadata(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt1")

    history_path = campaign_path / "batt1" / "history"

    write_detailed(history_path / "UnknownSN_history_detailed.txt")

    campaign = load_campaign(campaign_path)

    assert campaign.name == "campaign"
    assert len(campaign.exports) == 2

    export = next(export for export in campaign.exports if export.role == "batt1")

    assert export.device is not None
    assert export.snapshot is not None

    assert export.device.barcode == "P224009002250028"
    assert export.device.manufacturer == "Pylon"
    assert export.device.model == "bmu"

    assert export.snapshot.board_version == "HP0115SV10R01"
    assert export.snapshot.firmware_version == "V3.2"
    assert export.snapshot.cell_count == 15
    assert export.snapshot.capacity_ah == 50.0
    assert export.snapshot.nominal_voltage_v == 48.0


def test_load_campaign_uses_event_detailed_when_history_is_missing(
    tmp_path: Path,
) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt1")

    event_path = campaign_path / "batt1" / "events"

    write_detailed(event_path / "UnknownSN_event_detailed.txt")

    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "batt1")

    assert export.device is not None
    assert export.snapshot is not None
    assert export.device.model == "bmu"


def test_load_campaign_loads_history(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt1")

    history_path = campaign_path / "batt1" / "history"

    write_detailed(history_path / "UnknownSN_history_detailed.txt")
    write_bmu_history(history_path / "UnknownSN_history.csv")
    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "batt1")

    assert len(export.history) == 1

    record = export.history[0]

    assert record.timestamp.year == 2026
    assert record.timestamp.month == 7
    assert record.timestamp.day == 13
    assert record.timestamp.hour == 12

    assert record.values["module_voltage"] == 48000
    assert record.values["module_temperature"] == 25
    assert record.values["temperature_low"] == 24
    assert record.values["temperature_high"] == 26
    assert record.values["cell_voltage_low"] == 3300
    assert record.values["cell_voltage_high"] == 3310


def test_load_campaign_loads_bms_history(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")

    history_path = campaign_path / "BMS" / "history"

    write_detailed(
        history_path / "UnknownSN_history_detailed.txt",
        device_name="CMU_A",
    )
    write_bms_history(history_path / "UnknownSN_history.csv")

    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "BMS")

    assert export.device is not None
    assert export.device.model == "CMU_A"

    assert len(export.history) == 1

    record = export.history[0]

    assert record.values["stack_voltage"] == 48000
    assert record.values["stack_current"] == 1000
    assert record.values["temperature"] == 25
    assert record.values["state_of_charge"] == 100


def test_load_campaign_loads_xhb_bmu_history(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt2")

    history_path = campaign_path / "batt2" / "history"

    write_detailed(
        history_path / "UnknownSN_history_detailed.txt",
        device_name="XHB_BMU_NT",
    )
    write_xhb_bmu_history(history_path / "UnknownSN_history.csv")

    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "batt2")

    assert export.device is not None
    assert export.device.model == "XHB_BMU_NT"

    assert len(export.history) == 1

    record = export.history[0]

    assert record.timestamp == datetime(2026, 7, 13, 12, 0, 0)

    assert record.values["module_voltage"] == 48000
    assert record.values["module_temperature"] == 25
    assert record.values["battery_temp_low"] == 24
    assert record.values["battery_temp_high"] == 26
    assert record.values["battery_voltage_low"] == 48000
    assert record.values["battery_voltage_high"] == 48100
    assert record.values["positive_temperature"] == 25
    assert record.values["negative_temperature"] == 26
    assert record.values["reference_voltage"] == 3300
    assert record.values["fan_pwm"] == 3400
    assert record.values["fan1_rpm"] == 5000
    assert record.values["fan2_rpm"] == 50


def test_load_campaign_loads_bmu_events(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt1")

    write_detailed(
        campaign_path / "batt1" / "history" / "UnknownSN_history_detailed.txt",
        device_name="bmu",
    )
    write_bmu_events(campaign_path / "batt1" / "events" / "UnknownSN_event.csv")

    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "batt1")

    assert len(export.events) == 1

    event = export.events[0]

    assert event.timestamp == datetime(2026, 7, 13, 12, 0, 0)
    assert event.event_code == "0"

    assert event.values["module_voltage"] == 48000
    assert event.values["module_temperature"] == 25
    assert event.values["temperature_low"] == 24
    assert event.values["temperature_high"] == 26
    assert event.values["cell_voltage_low"] == 3300
    assert event.values["cell_voltage_high"] == 3310


def test_load_campaign_loads_bms_events(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")

    write_bms_history_for_events(
        campaign_path / "BMS" / "history" / "UnknownSN_history.csv"
    )

    write_detailed(
        campaign_path / "BMS" / "history" / "UnknownSN_history_detailed.txt",
        device_name="CMU_A",
    )
    write_bms_events(campaign_path / "BMS" / "events" / "UnknownSN_event.csv")

    campaign = load_campaign(campaign_path)

    export = campaign.bms

    assert export is not None
    assert len(export.events) == 1

    event = export.events[0]

    assert event.timestamp == datetime(2026, 7, 13, 12, 0, 0)
    assert event.event_code == "123"

    assert event.values["stack_voltage"] == 48000
    assert event.values["stack_current"] == 1000
    assert event.values["temperature"] == 25
    assert event.values["battery_temp_low"] == 24
    assert event.values["battery_temp_high"] == 26
    assert event.values["battery_voltage_low"] == 48000
    assert event.values["battery_voltage_high"] == 48100
    assert event.values["state_of_charge"] == 100
    assert event.values["error_code"] == "0"
    assert event.values["battery_events"] == "456"
    assert event.values["unit_events"] == "789"


def test_load_campaign_loads_xhb_bmu_events(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign"

    create_minimal_export(campaign_path / "BMS")
    create_minimal_export(campaign_path / "batt2")

    write_xhb_bmu_history_for_events(
        campaign_path / "batt2" / "history" / "UnknownSN_history.csv"
    )

    write_detailed(
        campaign_path / "batt2" / "history" / "UnknownSN_history_detailed.txt",
        device_name="XHB_BMU_NT",
    )
    write_xhb_bmu_events(campaign_path / "batt2" / "events" / "UnknownSN_event.csv")

    campaign = load_campaign(campaign_path)

    export = next(export for export in campaign.exports if export.role == "batt2")

    assert len(export.events) == 1

    event = export.events[0]

    assert event.timestamp == datetime(2026, 7, 13, 12, 0, 0)
    assert event.event_code == "123"

    assert event.values["module_voltage"] == 48000
    assert event.values["module_temperature"] == 25
    assert event.values["temperature_low"] == 24
    assert event.values["temperature_high"] == 26
    assert event.values["cell_voltage_low"] == 3300
    assert event.values["cell_voltage_high"] == 3400
    assert event.values["positive_terminal_temperature"] == 5000
    assert event.values["negative_terminal_temperature"] == 50
    assert event.values["reference_voltage"] == 1000
    assert event.values["fan_pwm"] == 1100
