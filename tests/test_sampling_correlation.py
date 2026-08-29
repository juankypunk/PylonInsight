from datetime import datetime, timedelta

from pyloninsight.analytics.sampling import analyze_sampling_interval
from pyloninsight.models.history import History


def make_record(timestamp, values):
    return History(
        timestamp=timestamp,
        values=values,
    )


def test_interval_and_voltage_change():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        {
            "module_voltage": 50000,
            "module_temperature": 40000,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "",
            "battery_events": "",
        },
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 1),
        {
            "module_voltage": 51000,
            "module_temperature": 41000,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "",
            "battery_events": "",
        },
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(
        minutes=30,
        seconds=1,
    )

    assert result.deviation == timedelta(seconds=1)

    assert result.module_voltage_before == 50000
    assert result.module_voltage_after == 51000
    assert result.module_voltage_delta == 1000

    assert result.module_temperature_before == 40000
    assert result.module_temperature_after == 41000
    assert result.module_temperature_delta == 1000

    assert result.voltage_state_before == "Normal"
    assert result.voltage_state_after == "Normal"

    assert result.temperature_state_before == "Normal"
    assert result.temperature_state_after == "Normal"

    assert result.events_before == ""
    assert result.events_after == ""

    assert result.battery_events_before == ""
    assert result.battery_events_after == ""

    print("PASS: test_interval_and_voltage_change")


def test_negative_voltage_delta():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        {
            "module_voltage": 51000,
            "module_temperature": 40000,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "",
            "battery_events": "",
        },
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        {
            "module_voltage": 50000,
            "module_temperature": 39000,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "",
            "battery_events": "",
        },
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_delta == -1000
    assert result.module_temperature_delta == -1000

    print("PASS: test_negative_voltage_delta")


def test_no_timestamps():
    previous = make_record(
        None,
        {
            "module_voltage": 50000,
        },
    )

    current = make_record(
        None,
        {
            "module_voltage": 51000,
        },
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval is None
    assert result.deviation is None

    assert result.module_voltage_before == 50000
    assert result.module_voltage_after == 51000
    assert result.module_voltage_delta == 1000

    print("PASS: test_no_timestamps")


def test_missing_optional_values():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        {
            "module_voltage": 50000,
        },
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        {
            "module_voltage": 51000,
        },
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(minutes=30)
    assert result.deviation == timedelta(0)

    assert result.module_voltage_delta == 1000

    assert result.module_temperature_before is None
    assert result.module_temperature_after is None
    assert result.module_temperature_delta is None

    assert result.events_before is None
    assert result.events_after is None

    print("PASS: test_missing_optional_values")


def test_xhb_error_code_and_battery_values():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        {
            "module_voltage": 50000,
            "module_temperature": 40000,
            "battery_temp_low": 35000,
            "battery_temp_high": 36000,
            "battery_voltage_low": 3300,
            "battery_voltage_high": 3350,
            "error_code": "0x0",
            "events": "",
        },
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 7, 30),
        {
            "module_voltage": 51000,
            "module_temperature": 41000,
            "battery_temp_low": 36000,
            "battery_temp_high": 37000,
            "battery_voltage_low": 3400,
            "battery_voltage_high": 3450,
            "error_code": "0x20",
            "events": "SYSERR",
        },
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=7, seconds=30),
    )

    assert result.interval == timedelta(
        minutes=7,
        seconds=30,
    )

    assert result.deviation == timedelta(0)

    assert result.module_voltage_delta == 1000
    assert result.module_temperature_delta == 1000

    assert result.battery_temp_low_before == 35000
    assert result.battery_temp_low_after == 36000
    assert result.battery_temp_low_delta == 1000

    assert result.battery_temp_high_before == 36000
    assert result.battery_temp_high_after == 37000
    assert result.battery_temp_high_delta == 1000

    assert result.battery_voltage_low_before == 3300
    assert result.battery_voltage_low_after == 3400
    assert result.battery_voltage_low_delta == 100

    assert result.battery_voltage_high_before == 3350
    assert result.battery_voltage_high_after == 3450
    assert result.battery_voltage_high_delta == 100

    assert result.error_code_before == "0x0"
    assert result.error_code_after == "0x20"

    assert result.events_before == ""
    assert result.events_after == "SYSERR"

    print("PASS: test_xhb_error_code_and_battery_values")


def test_records_are_not_modified():
    previous_values = {
        "module_voltage": 50000,
        "module_temperature": 40000,
        "voltage_state": "Normal",
        "temperature_state": "Normal",
        "events": "",
        "battery_events": "",
    }

    current_values = {
        "module_voltage": 51000,
        "module_temperature": 41000,
        "voltage_state": "Normal",
        "temperature_state": "Normal",
        "events": "",
        "battery_events": "",
    }

    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        previous_values.copy(),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        current_values.copy(),
    )

    previous_original = previous.values.copy()
    current_original = current.values.copy()

    analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert previous.values == previous_original
    assert current.values == current_original

    print("PASS: test_records_are_not_modified")


if __name__ == "__main__":
    test_interval_and_voltage_change()
    test_negative_voltage_delta()
    test_no_timestamps()
    test_missing_optional_values()
    test_xhb_error_code_and_battery_values()
    test_records_are_not_modified()

    print()
    print("6 tests passed.")
