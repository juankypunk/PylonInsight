from datetime import datetime
from pathlib import Path

from pyloninsight.common.datetime import extract_export_timestamp


def test_extract_export_timestamp_from_event_filename():
    path = Path("UnknownSN_event_20260713203051.csv")

    result = extract_export_timestamp(path)

    assert result == datetime(2026, 7, 13, 20, 30, 51)


def test_extract_export_timestamp_from_history_filename():
    path = Path("UnknownSN_history_20260713203142.csv")

    result = extract_export_timestamp(path)

    assert result == datetime(2026, 7, 13, 20, 31, 42)


def test_extract_export_timestamp_from_detailed_filename():
    path = Path("UnknownSN_history_detailed_20260713203142.txt")

    result = extract_export_timestamp(path)

    assert result == datetime(2026, 7, 13, 20, 31, 42)


def test_extract_export_timestamp_returns_none_when_missing():
    path = Path("UnknownSN_history.csv")

    result = extract_export_timestamp(path)

    assert result is None


def test_extract_export_timestamp_returns_none_for_invalid_timestamp():
    path = Path("UnknownSN_event_20261313203051.csv")

    result = extract_export_timestamp(path)

    assert result is None
