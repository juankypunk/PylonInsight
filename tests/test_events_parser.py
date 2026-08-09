from datetime import datetime
from pathlib import Path

from pyloninsight.parsers.events import parse_bms_events

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "real"
    / "2026-07-13_SOC100"
    / "BMS"
    / "events"
    / "H220829100140097_event_20260713201930.csv"
)


def test_record_count(records):
    assert len(records) == 384


def test_first_timestamp(records):
    assert records[0].timestamp == datetime(2026, 2, 20, 20, 47, 17)


def test_last_timestamp(records):
    assert records[-1].timestamp == datetime(2026, 7, 13, 21, 16, 4)


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

    actual_fields = set(records[0].values.keys())

    assert actual_fields == expected_fields


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
        value = records[0].values[field]

        assert isinstance(value, int)


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

    for record in records:
        for field in text_fields:
            assert isinstance(record.values[field], str)


def test_records_are_chronological(records):
    timestamps = [record.timestamp for record in records]

    assert timestamps == sorted(timestamps)


def test_event_codes_are_preserved(records):
    event_codes = {record.event_code for record in records}

    assert "BHV" in event_codes
    assert "DSG" in event_codes
    assert "BLV" in event_codes
    assert "SYSERR" in event_codes


def test_bhv_event_is_preserved(records):
    bhv_events = [record for record in records if record.event_code == "BHV"]

    assert len(bhv_events) > 0


def test_dsg_event_is_preserved(records):
    dsg_events = [record for record in records if record.event_code == "DSG"]

    assert len(dsg_events) > 0


def test_syserr_event_and_error_code_are_preserved(records):
    syserr_records = [
        record for record in records if record.values.get("events") == "SYSERR"
    ]

    assert len(syserr_records) > 0

    assert any(record.values.get("error_code") == "0x100" for record in syserr_records)


def test_event_objects(records):
    for record in records:
        assert record.timestamp is not None
        assert isinstance(record.values, dict)


def load_records():
    return parse_bms_events(DATA_FILE)


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
        test_event_codes_are_preserved,
        test_bhv_event_is_preserved,
        test_dsg_event_is_preserved,
        test_syserr_event_and_error_code_are_preserved,
        test_event_objects,
    ]

    for test in tests:
        test(records)
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
