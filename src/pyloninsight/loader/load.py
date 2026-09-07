from __future__ import annotations

from pathlib import Path

from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.parsers.detailed import parse_detailed
from pyloninsight.parsers.history import parse_bms_history
from pyloninsight.parsers.history_bmu import parse_bmu_history
from pyloninsight.parsers.history_xhb_bmu import parse_xhb_bmu_history

from pyloninsight.parsers.events import parse_bms_events
from pyloninsight.parsers.events_bmu import parse_bmu_events
from pyloninsight.parsers.events_xhb_bmu import parse_xhb_bmu_events

HISTORY_PARSERS = {
    "CMU_A": parse_bms_history,
    "bmu": parse_bmu_history,
    "XHB_BMU_NT": parse_xhb_bmu_history,
}

EVENT_PARSERS = {
    "CMU_A": parse_bms_events,
    "bmu": parse_bmu_events,
    "XHB_BMU_NT": parse_xhb_bmu_events,
}


def load_campaign(path: Path) -> Campaign:
    """
    Discover and load a BatteryView campaign.

    The loader currently loads:
        - device metadata from detailed.txt
        - device snapshots
        - history records

    Event data is loaded by a later stage.
    """
    from pyloninsight.discovery.discover import discover_campaign

    campaign = discover_campaign(path)

    for export in campaign.exports:
        _load_export(export)

    return campaign


def _load_export(export: CampaignExport) -> None:
    """
    Load all currently supported data for one campaign export.
    """
    _load_export_metadata(export)
    _load_export_history(export)
    _load_export_events(export)


def _load_export_metadata(export: CampaignExport) -> None:
    """
    Load Device and DeviceSnapshot information for one campaign export.
    """
    detailed = export.files.history_detailed

    if detailed is None:
        detailed = export.files.event_detailed

    if detailed is None:
        return

    device, snapshot = parse_detailed(detailed)

    export.device = device
    export.snapshot = snapshot


def _load_export_history(export: CampaignExport) -> None:
    """
    Load history records using the parser appropriate for the device model.
    """
    if export.device is None:
        return

    history_path = export.files.history_csv

    if history_path is None:
        return

    parser = HISTORY_PARSERS.get(export.device.model)

    if parser is None:
        return

    export.history = parser(history_path)


def _load_export_events(export: CampaignExport) -> None:
    """
    Load event records using the parser appropriate for the device model.
    """
    if export.device is None:
        return

    event_path = export.files.event_csv
    if event_path is None:
        return

    if event_path.stat().st_size == 0:
        return

    parser = EVENT_PARSERS.get(export.device.model)
    if parser is None:
        return

    export.events = parser(event_path)
