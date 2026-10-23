from __future__ import annotations

import psycopg
from psycopg.types.json import Jsonb
from pyloninsight.models.device_snapshot import DeviceSnapshot


class DeviceSnapshotRepository:
    """Persistence operations for DeviceSnapshot objects."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create(
        self,
        campaign_export_id: int,
        snapshot: DeviceSnapshot,
    ) -> int:
        """Create a device snapshot and return its database ID."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO device_snapshot (
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
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
                """,
                (
                    campaign_export_id,
                    snapshot.snapshot_timestamp,
                    snapshot.board_version,
                    snapshot.hardware_version,
                    snapshot.main_soft_version,
                    snapshot.soft_version,
                    snapshot.sub_soft_version,
                    snapshot.boot_version,
                    snapshot.comm_version,
                    snapshot.manufacture_date_aprox,
                    snapshot.release_date,
                    snapshot.battery_type,
                    snapshot.chemistry,
                    snapshot.cell_count,
                    snapshot.capacity_ah,
                    snapshot.nominal_voltage_v,
                    snapshot.module_afetype,
                    snapshot.module_celltype,
                    snapshot.fan_exist,
                    snapshot.xhb_v3_board,
                    (
                        Jsonb(snapshot.additional)
                        if snapshot.additional is not None
                        else None
                    ),
                ),
            )

            snapshot_id = cursor.fetchone()[0]


        return snapshot_id

    def get_by_id(self, snapshot_id: int) -> DeviceSnapshot | None:
        """Return a device snapshot by database ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
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
                (snapshot_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        (
            _,
            _campaign_export_id,
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
            additional,
        ) = row

        return DeviceSnapshot(
            snapshot_timestamp=snapshot_timestamp,
            board_version=board_version,
            hardware_version=hardware_version,
            main_soft_version=main_soft_version,
            soft_version=soft_version,
            sub_soft_version=sub_soft_version,
            boot_version=boot_version,
            comm_version=comm_version,
            manufacture_date_aprox=manufacture_date_aprox,
            release_date=release_date,
            battery_type=battery_type,
            chemistry=chemistry,
            cell_count=cell_count,
            capacity_ah=float(capacity_ah) if capacity_ah is not None else None,
            nominal_voltage_v=(
                float(nominal_voltage_v) if nominal_voltage_v is not None else None
            ),
            module_afetype=module_afetype,
            module_celltype=module_celltype,
            fan_exist=fan_exist,
            xhb_v3_board=xhb_v3_board,
            additional=additional,
        )
