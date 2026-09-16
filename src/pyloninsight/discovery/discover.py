from pathlib import Path
from datetime import datetime
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.common.datetime import extract_export_timestamp
from .errors import InvalidCampaignError
from .filesystem import discover_export_files


def _get_capture_date(exports: list[CampaignExport]):
    """
    Return the earliest timestamp found in the export files.

    The campaign capture date is defined as the earliest valid
    BatteryView export timestamp found across all devices.

    Returns:
        The earliest timestamp, or None if no valid timestamp is found.
    """
    timestamps = []

    for export in exports:
        files = export.files

        for path in (
            files.history_csv,
            files.history_txt,
            files.history_detailed,
            files.event_csv,
            files.event_txt,
            files.event_detailed,
        ):
            if path is None:
                continue

            timestamp = extract_export_timestamp(path)

            if timestamp is not None:
                timestamps.append(timestamp)

    if not timestamps:
        return None

    return min(timestamps)


def _get_export_timestamp(export: CampaignExport) -> datetime | None:
    """
    Return the earliest timestamp found in an export's files.
    """
    timestamps = []

    files = export.files

    for path in (
        files.history_csv,
        files.history_txt,
        files.history_detailed,
        files.event_csv,
        files.event_txt,
        files.event_detailed,
    ):
        if path is None:
            continue

        timestamp = extract_export_timestamp(path)

        if timestamp is not None:
            timestamps.append(timestamp)

    if not timestamps:
        return None

    return min(timestamps)


def discover_campaign(path: Path) -> Campaign:
    """
    Discover the structure of a BatteryView campaign.

    This stage discovers the devices and their exported files.
    No CSV or TXT files are parsed.
    """

    if not path.is_dir():
        raise InvalidCampaignError(f"Campaign directory does not exist: {path}")

    device_dirs = sorted(
        directory for directory in path.iterdir() if directory.is_dir()
    )

    bms_dirs = [
        directory for directory in device_dirs if directory.name.upper() == "BMS"
    ]

    if len(bms_dirs) == 0:
        raise InvalidCampaignError(f"Campaign contains no BMS directory: {path}")

    if len(bms_dirs) > 1:
        raise InvalidCampaignError(
            f"Campaign contains multiple BMS directories: {path}"
        )

    campaign = Campaign(name=path.name)

    for device_dir in device_dirs:

        export = CampaignExport(
            role=device_dir.name,
            files=discover_export_files(device_dir),
        )

        export.export_timestamp = _get_export_timestamp(export)

        campaign.add_export(export)

    campaign.capture_date = _get_capture_date(campaign.exports)

    return campaign
