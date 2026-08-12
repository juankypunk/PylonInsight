from datetime import datetime
from pathlib import Path

from pyloninsight.parsers.history_xhb_bmu import parse_xhb_bmu_history

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "real"
    / "2026-07-13_SOC100"
    / "BMU2"
    / "history"
    / "UnknownSN_history_20260713203417.csv"
)


def test_record_count(records):
    assert len(records) == 1818


def test_first_timestamp(records):
    assert records[0].timestamp == datetime(2026, 7, 4, 15, 18, 41)


def test_last_timestamp(records):
    assert records[-1].timestamp == datetime(2026, 7, 14, 2, 31, 2)


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
        "battery_temp_low",
        "battery_temp_high",
        "battery_voltage_low",
        "battery_voltage_high",
        "positive_temperature",
        "negative_temperature",
        "reference_voltage",
        "fan_pwm",
        "fan1_rpm",
        "fan2_rpm",
        "base_state",
        "voltage_state",
        "temperature_state",
        "positive_temperature_state",
        "negative_temperature_state",
        "error_code",
        "events",
    }

    actual_fields = set(records[0].values.keys())

    assert actual_fields == expected_fields


def test_numeric_fields_are_integers(records):
    numeric_fields = {
        "module_voltage",
        "module_temperature",
        "battery_temp_low",
        "battery_temp_high",
        "battery_voltage_low",
        "battery_voltage_high",
        "positive_temperature",
        "negative_temperature",
        "reference_voltage",
        "fan_pwm",
        "fan1_rpm",
        "fan2_rpm",
    }

    for record in records:
        for field in numeric_fields:
            value = record.values[field]
            assert isinstance(value, int), (
                f"Campo: {field} | "
                f"Valor: {value!r} | "
                f"Tipo: {type(value).__name__}"
            )


def test_text_fields_are_strings(records):
    text_fields = {
        "base_state",
        "voltage_state",
        "temperature_state",
        "positive_temperature_state",
        "negative_temperature_state",
        "error_code",
        "events",
    }

    for record in records:
        for field in text_fields:
            value = record.values[field]
            assert isinstance(value, str), (
                f"Campo: {field} | "
                f"Valor: {value!r} | "
                f"Tipo: {type(value).__name__}"
            )


def test_invalid_timestamp_is_preserved(records):
    invalid_records = [record for record in records if record.timestamp is None]

    assert len(invalid_records) == 1

    record = invalid_records[0]

    assert record.values["module_voltage"] == 50528
    assert record.values["battery_temp_low"] == 35000
    assert record.values["battery_temp_high"] == 36000
    assert record.values["battery_voltage_low"] == 3368
    assert record.values["battery_voltage_high"] == 3370


def test_invalid_timestamp_is_not_corrected(records):
    invalid_records = [record for record in records if record.timestamp is None]

    assert len(invalid_records) == 1

    record = invalid_records[0]

    assert record.timestamp is None


def test_history_objects(records):
    for record in records:
        assert record.values is not None
        assert isinstance(record.values, dict)


def load_records():
    return parse_xhb_bmu_history(DATA_FILE)


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
        test_invalid_timestamp_is_preserved,
        test_invalid_timestamp_is_not_corrected,
        test_history_objects,
    ]

    for test in tests:
        test(records)
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
