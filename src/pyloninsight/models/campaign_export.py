from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from .base import BaseModel
from .device import Device
from .device_snapshot import DeviceSnapshot
from .event import Event
from .history import History

from .export_files import ExportFiles


@dataclass(slots=True)
class CampaignExport(BaseModel):
    role: str
    export_timestamp: datetime | None = None
    device: Device | None = None
    snapshot: DeviceSnapshot | None = None
    files: ExportFiles = field(default_factory=ExportFiles)
    history: list[History] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
