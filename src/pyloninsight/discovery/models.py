@dataclass(slots=True)
class DiscoveredExport:

    role: str

    history_csv: Path | None
    history_txt: Path | None
    history_detailed: Path | None

    event_csv: Path | None
    event_txt: Path | None
    event_detailed: Path | None

    scanlog: Path | None