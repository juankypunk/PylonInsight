from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Campaign:
    """
    A BatteryView acquisition campaign.
    """

    name: str
    created_at: datetime | None = None
    description: str | None = None

    exports: list["CampaignExport"] = field(default_factory=list)