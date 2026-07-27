from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass(slots=True)
class Event(BaseModel):
    """
    One BatteryView event record.
    """

    timestamp: datetime

    event_code: str

    description: str | None = None

    values: dict | None = None