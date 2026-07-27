from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass(slots=True)
class DeviceSnapshot(BaseModel):
    """
    Device information captured during one campaign export.
    """

    timestamp: datetime | None = None

    board_version: str | None = None
    hardware_version: str | None = None
    firmware_version: str | None = None
    boot_version: str | None = None

    manufacture_date: date | None = None
    release_date: date | None = None

    battery_type: str | None = None
    chemistry: str | None = None

    cell_count: int | None = None
    capacity_ah: float | None = None
    nominal_voltage_v: float | None = None

    additional: dict | None = None