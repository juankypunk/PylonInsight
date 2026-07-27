from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel
from .campaign_export import CampaignExport


@dataclass(slots=True)
class Campaign(BaseModel):
    """
    Complete BatteryView acquisition campaign.
    """

    name: str

    created_at: datetime | None = None

    description: str | None = None

    exports: list[CampaignExport] = field(default_factory=list)

    def add_export(self, export: CampaignExport) -> None:
        self.exports.append(export)

    @property
    def devices(self):
        return [export.device for export in self.exports]

    @property
    def bms(self):
        for export in self.exports:
            if export.role.upper() == "BMS":
                return export
        return None

    @property
    def battery_modules(self):
        return [
            export
            for export in self.exports
            if export.role.upper() != "BMS"
        ]