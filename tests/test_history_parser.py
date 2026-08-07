from datetime import datetime
from pathlib import Path

from pyloninsight.parsers.history import parse_bms_history

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "real"
    / "2026-07-13_SOC100"
    / "BMS"
    / "history"
    / "H220829100140097_history_20260713202315.csv"
)


def test_record_count(records):
    assert len(records) == 512


def test_first_timestamp(records):
    assert records[0].timestamp == datetime(2026, 7, 3, 10, 26, 16)


def test_last_timestamp(records):
    assert records[-1].timestamp == datetime(2026, 7, 14, 1, 58, 34)


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
        "stack_voltage",
        "stack_current",
        "temperature",
        "battery_temp_low",
        "battery_temp_high",
        "battery_voltage_low",
        "battery_voltage_high",
        "unit_temp_low",
        "unit_temp_high",
        "unit_voltage_low",
        "unit_voltage_high",
        "base_state",
        "voltage_state",
        "current_state",
        "temperature_state",
        "state_of_charge",
        "error_code",
        "events",
        "battery_events",
        "unit_events",
    }

    assert set(records[0].values.keys()) == expected_fields


def test_numeric_fields_are_integers(records):
    numeric_fields = {
        "stack_voltage",
        "stack_current",
        "temperature",
        "battery_temp_low",
        "battery_temp_high",
        "battery_voltage_low",
        "battery_voltage_high",
        "unit_temp_low",
        "unit_temp_high",
        "unit_voltage_low",
        "unit_voltage_high",
        "state_of_charge",
    }

    for field in numeric_fields:
        assert isinstance(records[0].values[field], int)


def test_text_fields_are_strings(records):
    text_fields = {
        "base_state",
        "voltage_state",
        "current_state",
        "temperature_state",
        "error_code",
        "events",
        "battery_events",
        "unit_events",
    }

    for field in text_fields:
        assert isinstance(records[0].values[field], str)


def test_records_are_chronological(records):
    timestamps = [record.timestamp for record in records]

    assert timestamps == sorted(timestamps)


def test_history_objects(records):
    for record in records:
        assert record.timestamp is not None
        assert isinstance(record.values, dict)


def test_empty_events_are_preserved(records):
    assert records[0].values["events"] == ""
    assert records[0].values["battery_events"] == ""
    assert records[0].values["unit_events"] == ""


def test_event_value_is_preserved(records):
    target_timestamp = datetime(2026, 7, 4, 14, 56, 14)

    record = next(record for record in records if record.timestamp == target_timestamp)

    assert record.values["events"] == "IDLE"
    assert record.values["battery_events"] == ""
    assert record.values["unit_events"] == ""


def load_records():
    return parse_bms_history(DATA_FILE)


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
        test_records_are_chronological,
        test_history_objects,
        test_empty_events_are_preserved,
        test_event_value_is_preserved,
    ]

    for test in tests:
        test(records)
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
