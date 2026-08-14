from datetime import datetime
from pathlib import Path

from pyloninsight.parsers.events_bmu import parse_bmu_events

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "real"
    / "2026-07-13_SOC100"
    / "BMU3"
    / "events"
    / "UnknownSN_event_20260713203732.csv"
)


def test_record_count(records):
    assert len(records) == 950


def test_first_timestamp(records):
    assert records[0].timestamp == datetime(2023, 1, 24, 17, 52, 47)


def test_last_timestamp(records):
    assert records[-1].timestamp == datetime(2026, 7, 14, 2, 25, 8)


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

    for record in records:
        for field in numeric_fields:
            value = record.values[field]
            assert isinstance(value, int)


def test_text_fields_are_strings(records):
    text_fields = {
        "voltage_state",
        "temperature_state",
        "events",
        "battery_events",
    }

    for record in records:
        for field in text_fields:
            value = record.values[field]
            assert isinstance(value, str)


def test_bhv_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "BHV"]

    assert events


def test_bvnor_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "BVNOR"]

    assert events


def test_phv_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "PHV"]

    assert events


def test_pvnor_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "PVNOR"]

    assert events


def test_syserr_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "SYSERR"]

    assert events


def test_idle_event_is_preserved(records):
    events = [record for record in records if record.values["events"] == "IDLE"]

    assert events


def test_event_objects(records):
    for record in records:
        assert record.timestamp is not None
        assert isinstance(record.values, dict)


def load_records():
    return parse_bmu_events(DATA_FILE)


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
        test_bhv_event_is_preserved,
        test_bvnor_event_is_preserved,
        test_phv_event_is_preserved,
        test_pvnor_event_is_preserved,
        test_syserr_event_is_preserved,
        test_idle_event_is_preserved,
        test_event_objects,
    ]

    for test in tests:
        test(records)
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
