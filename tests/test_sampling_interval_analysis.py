from datetime import datetime, timedelta

from pyloninsight.analytics.sampling import analyze_sampling_interval
from pyloninsight.models.history import History


def make_record(
    timestamp,
    *,
    module_voltage=None,
    module_temperature=None,
    voltage_state=None,
    temperature_state=None,
    events=None,
    battery_events=None,
    battery_temp_low=None,
    battery_temp_high=None,
    battery_voltage_low=None,
    battery_voltage_high=None,
    error_code=None,
):
    values = {}

    if module_voltage is not None:
        values["module_voltage"] = module_voltage

    if module_temperature is not None:
        values["module_temperature"] = module_temperature

    if voltage_state is not None:
        values["voltage_state"] = voltage_state

    if temperature_state is not None:
        values["temperature_state"] = temperature_state

    if events is not None:
        values["events"] = events

    if battery_events is not None:
        values["battery_events"] = battery_events

    if battery_temp_low is not None:
        values["battery_temp_low"] = battery_temp_low

    if battery_temp_high is not None:
        values["battery_temp_high"] = battery_temp_high

    if battery_voltage_low is not None:
        values["battery_voltage_low"] = battery_voltage_low

    if battery_voltage_high is not None:
        values["battery_voltage_high"] = battery_voltage_high

    if error_code is not None:
        values["error_code"] = error_code

    return History(
        timestamp=timestamp,
        values=values,
    )


def test_regular_sampling_interval():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(minutes=30)
    assert result.deviation == timedelta(0)

    print("PASS: test_regular_sampling_interval")


def test_sampling_interval_with_positive_deviation():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 31, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(minutes=31)
    assert result.deviation == timedelta(minutes=1)

    print("PASS: test_sampling_interval_with_positive_deviation")


def test_sampling_interval_with_negative_deviation():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 29, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(minutes=29)
    assert result.deviation == timedelta(minutes=-1)

    print("PASS: test_sampling_interval_with_negative_deviation")


def test_previous_timestamp_is_none():
    previous = make_record(None)

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval is None
    assert result.deviation is None

    print("PASS: test_previous_timestamp_is_none")


def test_current_timestamp_is_none():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    current = make_record(None)

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval is None
    assert result.deviation is None

    print("PASS: test_current_timestamp_is_none")


def test_both_timestamps_are_none():
    previous = make_record(None)
    current = make_record(None)

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval is None
    assert result.deviation is None

    print("PASS: test_both_timestamps_are_none")


def test_numeric_values_and_deltas():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        module_voltage=50000,
        module_temperature=250,
        battery_temp_low=200,
        battery_temp_high=300,
        battery_voltage_low=49000,
        battery_voltage_high=51000,
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        module_voltage=49900,
        module_temperature=260,
        battery_temp_low=205,
        battery_temp_high=295,
        battery_voltage_low=48900,
        battery_voltage_high=51100,
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_before == 50000
    assert result.module_voltage_after == 49900
    assert result.module_voltage_delta == -100

    assert result.module_temperature_before == 250
    assert result.module_temperature_after == 260
    assert result.module_temperature_delta == 10

    assert result.battery_temp_low_before == 200
    assert result.battery_temp_low_after == 205
    assert result.battery_temp_low_delta == 5

    assert result.battery_temp_high_before == 300
    assert result.battery_temp_high_after == 295
    assert result.battery_temp_high_delta == -5

    assert result.battery_voltage_low_before == 49000
    assert result.battery_voltage_low_after == 48900
    assert result.battery_voltage_low_delta == -100

    assert result.battery_voltage_high_before == 51000
    assert result.battery_voltage_high_after == 51100
    assert result.battery_voltage_high_delta == 100

    print("PASS: test_numeric_values_and_deltas")


def test_text_values_are_preserved():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        voltage_state="NORMAL",
        temperature_state="NORMAL",
        events="IDLE",
        battery_events="NONE",
        error_code="0000",
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        voltage_state="WARNING",
        temperature_state="HIGH",
        events="BHV",
        battery_events="SYSERR",
        error_code="1234",
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.voltage_state_before == "NORMAL"
    assert result.voltage_state_after == "WARNING"

    assert result.temperature_state_before == "NORMAL"
    assert result.temperature_state_after == "HIGH"

    assert result.events_before == "IDLE"
    assert result.events_after == "BHV"

    assert result.battery_events_before == "NONE"
    assert result.battery_events_after == "SYSERR"

    assert result.error_code_before == "0000"
    assert result.error_code_after == "1234"

    print("PASS: test_text_values_are_preserved")


def test_missing_values_are_none():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_before is None
    assert result.module_voltage_after is None
    assert result.module_voltage_delta is None

    assert result.module_temperature_before is None
    assert result.module_temperature_after is None
    assert result.module_temperature_delta is None

    assert result.voltage_state_before is None
    assert result.voltage_state_after is None

    assert result.temperature_state_before is None
    assert result.temperature_state_after is None

    assert result.events_before is None
    assert result.events_after is None

    assert result.battery_events_before is None
    assert result.battery_events_after is None

    assert result.battery_temp_low_before is None
    assert result.battery_temp_low_after is None
    assert result.battery_temp_low_delta is None

    assert result.battery_temp_high_before is None
    assert result.battery_temp_high_after is None
    assert result.battery_temp_high_delta is None

    assert result.battery_voltage_low_before is None
    assert result.battery_voltage_low_after is None
    assert result.battery_voltage_low_delta is None

    assert result.battery_voltage_high_before is None
    assert result.battery_voltage_high_after is None
    assert result.battery_voltage_high_delta is None

    assert result.error_code_before is None
    assert result.error_code_after is None

    print("PASS: test_missing_values_are_none")


def test_missing_value_on_one_side_produces_none_delta():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        module_voltage=50000,
        module_temperature=250,
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        module_temperature=260,
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_before == 50000
    assert result.module_voltage_after is None
    assert result.module_voltage_delta is None

    assert result.module_temperature_before == 250
    assert result.module_temperature_after == 260
    assert result.module_temperature_delta == 10

    print("PASS: test_missing_value_on_one_side_produces_none_delta")


def test_zero_values_are_valid():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        module_voltage=0,
        module_temperature=0,
        battery_temp_low=0,
        battery_temp_high=0,
        battery_voltage_low=0,
        battery_voltage_high=0,
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        module_voltage=100,
        module_temperature=10,
        battery_temp_low=5,
        battery_temp_high=15,
        battery_voltage_low=50,
        battery_voltage_high=150,
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_before == 0
    assert result.module_voltage_after == 100
    assert result.module_voltage_delta == 100

    assert result.module_temperature_before == 0
    assert result.module_temperature_after == 10
    assert result.module_temperature_delta == 10

    assert result.battery_temp_low_before == 0
    assert result.battery_temp_low_after == 5
    assert result.battery_temp_low_delta == 5

    assert result.battery_temp_high_before == 0
    assert result.battery_temp_high_after == 15
    assert result.battery_temp_high_delta == 15

    assert result.battery_voltage_low_before == 0
    assert result.battery_voltage_low_after == 50
    assert result.battery_voltage_low_delta == 50

    assert result.battery_voltage_high_before == 0
    assert result.battery_voltage_high_after == 150
    assert result.battery_voltage_high_delta == 150

    print("PASS: test_zero_values_are_valid")


def test_negative_values_are_valid():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        module_voltage=-100,
        module_temperature=-20,
        battery_temp_low=-30,
        battery_temp_high=-10,
        battery_voltage_low=-200,
        battery_voltage_high=-100,
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        module_voltage=-50,
        module_temperature=-10,
        battery_temp_low=-25,
        battery_temp_high=-5,
        battery_voltage_low=-150,
        battery_voltage_high=-50,
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.module_voltage_delta == 50
    assert result.module_temperature_delta == 10

    assert result.battery_temp_low_delta == 5
    assert result.battery_temp_high_delta == 5

    assert result.battery_voltage_low_delta == 50
    assert result.battery_voltage_high_delta == 50

    print("PASS: test_negative_values_are_valid")


def test_subsecond_precision_is_preserved():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0, 100000),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0, 250000),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(
        minutes=30,
        microseconds=150000,
    )

    assert result.deviation == timedelta(
        microseconds=150000,
    )

    print("PASS: test_subsecond_precision_is_preserved")


def test_records_are_not_modified():
    previous = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
        module_voltage=50000,
        module_temperature=250,
        voltage_state="NORMAL",
        events="IDLE",
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
        module_voltage=49900,
        module_temperature=260,
        voltage_state="WARNING",
        events="BHV",
    )

    previous_timestamp = previous.timestamp
    previous_values = dict(previous.values)

    current_timestamp = current.timestamp
    current_values = dict(current.values)

    analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert previous.timestamp == previous_timestamp
    assert previous.values == previous_values

    assert current.timestamp == current_timestamp
    assert current.values == current_values

    print("PASS: test_records_are_not_modified")


def test_timestamp_regression_is_reported_as_negative_interval():
    previous = make_record(
        datetime(2026, 7, 1, 10, 30, 0),
    )

    current = make_record(
        datetime(2026, 7, 1, 10, 0, 0),
    )

    result = analyze_sampling_interval(
        previous,
        current,
        expected_interval=timedelta(minutes=30),
    )

    assert result.interval == timedelta(minutes=-30)
    assert result.deviation == timedelta(minutes=-60)

    print("PASS: test_timestamp_regression_is_reported_as_negative_interval")


if __name__ == "__main__":
    test_regular_sampling_interval()
    test_sampling_interval_with_positive_deviation()
    test_sampling_interval_with_negative_deviation()
    test_previous_timestamp_is_none()
    test_current_timestamp_is_none()
    test_both_timestamps_are_none()
    test_numeric_values_and_deltas()
    test_text_values_are_preserved()
    test_missing_values_are_none()
    test_missing_value_on_one_side_produces_none_delta()
    test_zero_values_are_valid()
    test_negative_values_are_valid()
    test_subsecond_precision_is_preserved()
    test_records_are_not_modified()
    test_timestamp_regression_is_reported_as_negative_interval()

    print()
    print("15 tests passed.")
