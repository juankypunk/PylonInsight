from datetime import datetime
from pathlib import Path

from pyloninsight.parsers.history_bmu import parse_bmu_history

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "real"
    / "2026-07-13_SOC100"
    / "BMU3"
    / "history"
    / "UnknownSN_history_20260713203804.csv"
)


def test_record_count(records):
    assert len(records) == 2046


def test_first_timestamp(records):
    assert records[0].timestamp == datetime(2026, 6, 1, 12, 7, 18)


def test_last_timestamp(records):
    assert records[-1].timestamp == datetime(2026, 7, 14, 2, 29, 36)


def test_item_is_not_in_values(records):
    assert "Item" not in records[0].values
    assert "record_index" not in records[0].values


def test_date_and_time_are_not_in_values(records):
    assert "Date" not in records[0].values
    assert "Time" not in records[0].values
    assert "record_date" not in records[0].values
    assert "record_time" not in records[0].values


def test_canonical_field_names(records):
    expected_fields = {
        "module_voltage",
        "module_temperature",
        "temperature_low",
        "temperature_high",
        "cell_voltage_low",
        "cell_voltage_high",
        "voltage_state",
        "temperature_state",
        "events",
        "battery_events",
    }

    assert set(records[0].values.keys()) == expected_fields


def test_numeric_fields_are_integers(records):
    numeric_fields = {
        "module_voltage",
        "module_temperature",
        "temperature_low",
        "temperature_high",
        "cell_voltage_low",
        "cell_voltage_high",
    }

    for field in numeric_fields:
        assert isinstance(records[0].values[field], int)


def test_text_fields_are_strings(records):
    text_fields = {
        "voltage_state",
        "temperature_state",
        "events",
        "battery_events",
    }

    for field in text_fields:
        assert isinstance(records[0].values[field], str)


def test_anomalous_timestamp_is_preserved(records):
    assert records[350].timestamp == datetime(2026, 6, 8, 19, 7, 4)

    assert records[351].timestamp == datetime(2022, 6, 4, 11, 21, 16)

    assert records[352].timestamp == datetime(2026, 6, 8, 19, 56, 39)


def test_anomalous_timestamp_is_not_corrected(records):
    assert records[351].timestamp.year == 2022
    assert records[351].timestamp.month == 6
    assert records[351].timestamp.day == 4


def test_history_objects(records):
    for record in records:
        assert record.timestamp is not None
        assert isinstance(record.values, dict)


def load_records():
    return parse_bmu_history(DATA_FILE)


if __name__ == "__main__":
    records = load_records()

    tests = [
        test_record_count,
        test_first_timestamp,
        test_last_timestamp,
        test_item_is_not_in_values,
        test_date_and_time_are_not_in_values,
        test_canonical_field_names,
        test_numeric_fields_are_integers,
        test_text_fields_are_strings,
        test_anomalous_timestamp_is_preserved,
        test_anomalous_timestamp_is_not_corrected,
        test_history_objects,
    ]

    for test in tests:
        test(records)
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
