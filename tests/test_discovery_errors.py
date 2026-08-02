from pathlib import Path

from pyloninsight.discovery import discover_campaign
from pyloninsight.discovery.errors import (
    DuplicateExportFileError,
    InvalidCampaignError,
    MissingDeviceExportError,
)

DATA_DIR = Path(__file__).parent / "data"
MALFORMED_DIR = DATA_DIR / "malformed"


def test_campaign_does_not_exist():
    path = MALFORMED_DIR / "does_not_exist"

    try:
        discover_campaign(path)
    except InvalidCampaignError:
        return

    raise AssertionError("Expected InvalidCampaignError")


def test_campaign_without_bms():
    path = MALFORMED_DIR / "no_bms"

    try:
        discover_campaign(path)
    except InvalidCampaignError:
        return

    raise AssertionError("Expected InvalidCampaignError")


def test_campaign_with_multiple_bms():
    path = MALFORMED_DIR / "multiple_bms"

    try:
        discover_campaign(path)
    except InvalidCampaignError:
        return

    raise AssertionError("Expected InvalidCampaignError")


def test_device_without_history():
    path = MALFORMED_DIR / "missing_history"

    try:
        discover_campaign(path)
    except MissingDeviceExportError:
        return

    raise AssertionError("Expected MissingDeviceExportError")


def test_device_without_events():
    path = MALFORMED_DIR / "missing_events"

    try:
        discover_campaign(path)
    except MissingDeviceExportError:
        return

    raise AssertionError("Expected MissingDeviceExportError")


def test_duplicate_history_csv():
    path = MALFORMED_DIR / "duplicate_history"

    try:
        discover_campaign(path)
    except DuplicateExportFileError:
        return

    raise AssertionError("Expected DuplicateExportFileError")


def test_duplicate_event_csv():
    path = MALFORMED_DIR / "duplicate_events"

    try:
        discover_campaign(path)
    except DuplicateExportFileError:
        return

    raise AssertionError("Expected DuplicateExportFileError")


def test_history_directory_without_csv():
    path = MALFORMED_DIR / "empty_history"

    try:
        discover_campaign(path)
    except MissingDeviceExportError:
        return

    raise AssertionError("Expected MissingDeviceExportError")


def test_events_directory_without_csv():
    path = MALFORMED_DIR / "empty_events"

    try:
        discover_campaign(path)
    except MissingDeviceExportError:
        return

    raise AssertionError("Expected MissingDeviceExportError")


if __name__ == "__main__":
    tests = [
        test_campaign_does_not_exist,
        test_campaign_without_bms,
        test_campaign_with_multiple_bms,
        test_device_without_history,
        test_device_without_events,
        test_duplicate_history_csv,
        test_duplicate_event_csv,
        test_history_directory_without_csv,
        test_events_directory_without_csv,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
