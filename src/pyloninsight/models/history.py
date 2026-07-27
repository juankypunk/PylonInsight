from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass(slots=True)
class History(BaseModel):
    """
    One history record exported by BatteryView.
    """

    timestamp: datetime

    values: dict