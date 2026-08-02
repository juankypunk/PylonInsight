from pathlib import Path

from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport

from .errors import InvalidCampaignError
from .filesystem import discover_export_files


def discover_campaign(path: Path) -> Campaign:
    """
    Discover the structure of a BatteryView campaign.

    This stage discovers the devices and their exported files.
    No CSV or TXT files are parsed.
    """

    if not path.is_dir():
        raise InvalidCampaignError(
            f"Campaign directory does not exist: {path}"
        )

    device_dirs = sorted(
        directory
        for directory in path.iterdir()
        if directory.is_dir()
    )

    bms_dirs = [
        directory
        for directory in device_dirs
        if directory.name.upper() == "BMS"
    ]

    if len(bms_dirs) == 0:
        raise InvalidCampaignError(
            f"Campaign contains no BMS directory: {path}"
        )

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

        campaign.add_export(export)

    return campaign