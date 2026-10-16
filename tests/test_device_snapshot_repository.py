from datetime import date, datetime
from unittest.mock import MagicMock
from psycopg.types.json import Jsonb
from pyloninsight.database.repositories.device_snapshot import (
    DeviceSnapshotRepository,
)
from pyloninsight.models.device_snapshot import DeviceSnapshot


def test_create_device_snapshot():
    cursor = MagicMock()
    cursor.fetchone.return_value = (15,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    snapshot_timestamp = datetime(2026, 7, 9, 10, 30)

    snapshot = DeviceSnapshot(
        snapshot_timestamp=snapshot_timestamp,
        board_version="HP0115SV10R01",
        hardware_version="V10R9C5",
        main_soft_version="B52.2.0",
        soft_version="V3.2",
        sub_soft_version="T1.0",
        boot_version="V1.4",
        comm_version="V2.0",
        manufacture_date_aprox=date(2021, 9, 29),
        release_date=date(2021, 9, 29),
        battery_type="H48050",
        chemistry="LFP",
        cell_count=15,
        capacity_ah=50.0,
        nominal_voltage_v=48.0,
        module_afetype="LTC6813",
        module_celltype="1",
        fan_exist=False,
        xhb_v3_board=False,
        additional={"source": "BatteryView"},
    )

    repository = DeviceSnapshotRepository(connection)

    snapshot_id = repository.create(
        campaign_export_id=12,
        snapshot=snapshot,
    )

    assert snapshot_id == 15

    cursor.execute.assert_called_once()

    args, kwargs = cursor.execute.call_args

    assert args[1][0:20] == (
        12,
        snapshot_timestamp,
        "HP0115SV10R01",
        "V10R9C5",
        "B52.2.0",
        "V3.2",
        "T1.0",
        "V1.4",
        "V2.0",
        date(2021, 9, 29),
        date(2021, 9, 29),
        "H48050",
        "LFP",
        15,
        50.0,
        48.0,
        "LTC6813",
        "1",
        False,
        False,
    )

    assert isinstance(args[1][20], Jsonb)
    assert args[1][20].obj == {"source": "BatteryView"}
    assert kwargs == {}


def test_get_device_snapshot_by_id():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        15,
        12,
        datetime(2026, 7, 9, 10, 30),
        "HP0115SV10R01",
        "V10R9C5",
        "B52.2.0",
        "V3.2",
        "T1.0",
        "V1.4",
        "V2.0",
        date(2021, 9, 29),
        date(2021, 9, 29),
        "H48050",
        "LFP",
        15,
        50.0,
        48.0,
        "LTC6813",
        "1",
        False,
        False,
        {"source": "BatteryView"},
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceSnapshotRepository(connection)

    snapshot = repository.get_by_id(15)

    assert snapshot is not None
    assert snapshot.snapshot_timestamp == datetime(2026, 7, 9, 10, 30)
    assert snapshot.board_version == "HP0115SV10R01"
    assert snapshot.hardware_version == "V10R9C5"
    assert snapshot.main_soft_version == "B52.2.0"
    assert snapshot.soft_version == "V3.2"
    assert snapshot.sub_soft_version == "T1.0"
    assert snapshot.boot_version == "V1.4"
    assert snapshot.comm_version == "V2.0"
    assert snapshot.manufacture_date_aprox == date(2021, 9, 29)
    assert snapshot.release_date == date(2021, 9, 29)
    assert snapshot.battery_type == "H48050"
    assert snapshot.chemistry == "LFP"
    assert snapshot.cell_count == 15
    assert snapshot.capacity_ah == 50.0
    assert snapshot.nominal_voltage_v == 48.0
    assert snapshot.module_afetype == "LTC6813"
    assert snapshot.module_celltype == "1"
    assert snapshot.fan_exist is False
    assert snapshot.xhb_v3_board is False
    assert snapshot.additional == {"source": "BatteryView"}

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    campaign_export_id,
                    snapshot_timestamp,
                    board_version,
                    hardware_version,
                    main_soft_version,
                    soft_version,
                    sub_soft_version,
                    boot_version,
                    comm_version,
                    manufacture_date_aprox,
                    release_date,
                    battery_type,
                    chemistry,
                    cell_count,
                    capacity_ah,
                    nominal_voltage_v,
                    module_afetype,
                    module_celltype,
                    fan_exist,
                    xhb_v3_board,
                    additional
                FROM device_snapshot
                WHERE id = %s
                """,
        (15,),
    )


def test_get_device_snapshot_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceSnapshotRepository(connection)

    snapshot = repository.get_by_id(999)

    assert snapshot is None

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    campaign_export_id,
                    snapshot_timestamp,
                    board_version,
                    hardware_version,
                    main_soft_version,
                    soft_version,
                    sub_soft_version,
                    boot_version,
                    comm_version,
                    manufacture_date_aprox,
                    release_date,
                    battery_type,
                    chemistry,
                    cell_count,
                    capacity_ah,
                    nominal_voltage_v,
                    module_afetype,
                    module_celltype,
                    fan_exist,
                    xhb_v3_board,
                    additional
                FROM device_snapshot
                WHERE id = %s
                """,
        (999,),
    )
