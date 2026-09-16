from datetime import datetime
from pathlib import Path
import re

_EXPORT_TIMESTAMP_PATTERN = re.compile(r"(?<!\d)(\d{14})(?!\d)")


def extract_export_timestamp(path: Path) -> datetime | None:
    """
    Extract the BatteryView export timestamp from a filename.

    BatteryView export filenames contain a timestamp in the form:
        YYYYMMDDHHMMSS

    Examples:
        UnknownSN_event_20260713203051.csv
        UnknownSN_history_20260713203142.csv

    Returns:
        A datetime object when a valid timestamp is found.
        None when no timestamp is present or the timestamp is invalid.
    """
    match = _EXPORT_TIMESTAMP_PATTERN.search(path.name)

    if match is None:
        return None

    try:
        return datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
    except ValueError:
        return None
