from dataclasses import dataclass
from datetime import date, datetime

from .base import BaseModel


@dataclass(slots=True)
class DeviceSnapshot(BaseModel):
    """
    Device information captured during one campaign export.
    """

    timestamp: datetime | None = None

    board_version: str | None = None
    hardware_version: str | None = None
    main_soft_version: str | None = None
    soft_version: str | None = None
    sub_soft_version: str | None = None
    boot_version: str | None = None
    comm_version: str | None = None

    manufacture_date_aprox: date | None = None
    release_date: date | None = None

    battery_type: str | None = None
    chemistry: str | None = None
    cell_count: int | None = None
    capacity_ah: float | None = None
    nominal_voltage_v: float | None = None

    module_afetype: str | None = None
    module_celltype: str | None = None
    fan_exist: bool | None = None
    xhb_v3_board: bool | None = None

    additional: dict | None = None
