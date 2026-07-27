from dataclasses import dataclass, field

from .base import BaseModel
from .device import Device
from .device_snapshot import DeviceSnapshot
from .event import Event
from .history import History


@dataclass(slots=True)
class CampaignExport(BaseModel):
    """
    Export of one physical device inside one BatteryView campaign.
    """

    role: str

    device: Device

    snapshot: DeviceSnapshot | None = None

    history: list[History] = field(default_factory=list)

    events: list[Event] = field(default_factory=list)

    scanlog_path: str | None = None