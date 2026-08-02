from dataclasses import dataclass
from pathlib import Path

from .base import BaseModel


@dataclass(slots=True)
class ExportFiles(BaseModel):
    """
    Physical files belonging to a single BatteryView export.

    This object is populated during the Discovery stage. It only stores
    filesystem paths; parsing is performed later by the corresponding
    parsers.
    """

    # History export
    history_csv: Path | None = None
    history_txt: Path | None = None
    history_detailed: Path | None = None

    # Event export
    event_csv: Path | None = None
    event_txt: Path | None = None
    event_detailed: Path | None = None

    # Optional scanlog export
    scanlog_csv: Path | None = None

    @property
    def has_history(self) -> bool:
        """Return True if a history export is available."""
        return self.history_csv is not None

    @property
    def has_events(self) -> bool:
        """Return True if an event export is available."""
        return self.event_csv is not None

    @property
    def has_scanlog(self) -> bool:
        """Return True if a scanlog export is available."""
        return self.scanlog_csv is not None

    @property
    def is_complete(self) -> bool:
        """
        Returns True if the mandatory BatteryView exports are present.
        """
        return self.has_history and self.has_events