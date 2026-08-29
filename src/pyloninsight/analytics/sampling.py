from collections import Counter
from dataclasses import dataclass
from datetime import timedelta

from pyloninsight.models.history import History


@dataclass
class SamplingStats:
    count: int
    minimum: timedelta | None
    maximum: timedelta | None
    median: timedelta | None
    mode: timedelta | None
    dominant_count: int
    dominant_percentage: float | None


@dataclass(frozen=True)
class SamplingGap:
    index: int
    interval: timedelta
    expected_interval: timedelta
    multiple: int


@dataclass
class SamplingIntervalAnalysis:
    interval: timedelta | None
    deviation: timedelta | None

    module_voltage_before: int | None
    module_voltage_after: int | None
    module_voltage_delta: int | None

    module_temperature_before: int | None
    module_temperature_after: int | None
    module_temperature_delta: int | None

    voltage_state_before: str | None
    voltage_state_after: str | None

    temperature_state_before: str | None
    temperature_state_after: str | None

    events_before: str | None
    events_after: str | None

    battery_events_before: str | None
    battery_events_after: str | None

    battery_temp_low_before: int | None
    battery_temp_low_after: int | None
    battery_temp_low_delta: int | None

    battery_temp_high_before: int | None
    battery_temp_high_after: int | None
    battery_temp_high_delta: int | None

    battery_voltage_low_before: int | None
    battery_voltage_low_after: int | None
    battery_voltage_low_delta: int | None

    battery_voltage_high_before: int | None
    battery_voltage_high_after: int | None
    battery_voltage_high_delta: int | None

    error_code_before: str | None
    error_code_after: str | None


def analyze_sampling_interval(
    previous: History,
    current: History,
    expected_interval: timedelta,
) -> SamplingIntervalAnalysis:
    """
    Analyze the relationship between a sampling interval and
    the changes in the values recorded before and after it.

    The function does not modify either record.

    Timestamp information:

    - interval:
        Actual time elapsed between the two records.
    - deviation:
        Difference between the actual interval and the expected
        sampling interval.

    Value information:

    For numeric fields, the function returns the value before,
    the value after, and their difference.

    Fields that are not present in a record are represented by None.
    """

    interval = None

    if previous.timestamp is not None and current.timestamp is not None:
        interval = current.timestamp - previous.timestamp

    deviation = None

    if interval is not None:
        deviation = interval - expected_interval

    previous_values = previous.values
    current_values = current.values

    def get_value(values, name):
        return values.get(name)

    def calculate_delta(before, after):
        if before is None or after is None:
            return None

        return after - before

    module_voltage_before = get_value(
        previous_values,
        "module_voltage",
    )

    module_voltage_after = get_value(
        current_values,
        "module_voltage",
    )

    module_temperature_before = get_value(
        previous_values,
        "module_temperature",
    )

    module_temperature_after = get_value(
        current_values,
        "module_temperature",
    )

    battery_temp_low_before = get_value(
        previous_values,
        "battery_temp_low",
    )

    battery_temp_low_after = get_value(
        current_values,
        "battery_temp_low",
    )

    battery_temp_high_before = get_value(
        previous_values,
        "battery_temp_high",
    )

    battery_temp_high_after = get_value(
        current_values,
        "battery_temp_high",
    )

    battery_voltage_low_before = get_value(
        previous_values,
        "battery_voltage_low",
    )

    battery_voltage_low_after = get_value(
        current_values,
        "battery_voltage_low",
    )

    battery_voltage_high_before = get_value(
        previous_values,
        "battery_voltage_high",
    )

    battery_voltage_high_after = get_value(
        current_values,
        "battery_voltage_high",
    )

    return SamplingIntervalAnalysis(
        interval=interval,
        deviation=deviation,
        module_voltage_before=module_voltage_before,
        module_voltage_after=module_voltage_after,
        module_voltage_delta=calculate_delta(
            module_voltage_before,
            module_voltage_after,
        ),
        module_temperature_before=module_temperature_before,
        module_temperature_after=module_temperature_after,
        module_temperature_delta=calculate_delta(
            module_temperature_before,
            module_temperature_after,
        ),
        voltage_state_before=get_value(
            previous_values,
            "voltage_state",
        ),
        voltage_state_after=get_value(
            current_values,
            "voltage_state",
        ),
        temperature_state_before=get_value(
            previous_values,
            "temperature_state",
        ),
        temperature_state_after=get_value(
            current_values,
            "temperature_state",
        ),
        events_before=get_value(
            previous_values,
            "events",
        ),
        events_after=get_value(
            current_values,
            "events",
        ),
        battery_events_before=get_value(
            previous_values,
            "battery_events",
        ),
        battery_events_after=get_value(
            current_values,
            "battery_events",
        ),
        battery_temp_low_before=battery_temp_low_before,
        battery_temp_low_after=battery_temp_low_after,
        battery_temp_low_delta=calculate_delta(
            battery_temp_low_before,
            battery_temp_low_after,
        ),
        battery_temp_high_before=battery_temp_high_before,
        battery_temp_high_after=battery_temp_high_after,
        battery_temp_high_delta=calculate_delta(
            battery_temp_high_before,
            battery_temp_high_after,
        ),
        battery_voltage_low_before=battery_voltage_low_before,
        battery_voltage_low_after=battery_voltage_low_after,
        battery_voltage_low_delta=calculate_delta(
            battery_voltage_low_before,
            battery_voltage_low_after,
        ),
        battery_voltage_high_before=battery_voltage_high_before,
        battery_voltage_high_after=battery_voltage_high_after,
        battery_voltage_high_delta=calculate_delta(
            battery_voltage_high_before,
            battery_voltage_high_after,
        ),
        error_code_before=get_value(
            previous_values,
            "error_code",
        ),
        error_code_after=get_value(
            current_values,
            "error_code",
        ),
    )


def find_sampling_gaps(
    intervals: list[timedelta],
    expected_interval: timedelta,
    tolerance: timedelta = timedelta(seconds=10),
) -> list[SamplingGap]:
    """
    Find sampling intervals that indicate one or more missing samples.

    A sampling gap is detected when an interval is sufficiently close
    to an integer multiple of the expected sampling interval and the
    multiple is greater than one.

    Small timing deviations are tolerated.

    The input list is not modified.
    """

    gaps = []

    if not intervals:
        return gaps

    if expected_interval <= timedelta(0):
        raise ValueError("expected_interval must be greater than zero")

    if tolerance < timedelta(0):
        raise ValueError("tolerance must not be negative")

    for index, interval in enumerate(intervals):

        if interval <= expected_interval:
            continue

        multiple = interval / expected_interval

        nearest_multiple = round(multiple)

        if nearest_multiple < 2:
            continue

        expected_gap = expected_interval * nearest_multiple

        difference = abs(interval - expected_gap)

        if difference <= tolerance:
            gaps.append(
                SamplingGap(
                    index=index,
                    interval=interval,
                    expected_interval=expected_interval,
                    multiple=nearest_multiple,
                )
            )

    return gaps


def calculate_sampling_intervals(
    records: list[History],
    anomalies=None,
) -> list[timedelta]:
    """
    Calculate the intervals between consecutive valid timestamps.

    Records with an invalid timestamp (None) are skipped.

    If history anomalies are supplied, timestamp regressions break
    the sampling sequence. No interval is generated across a
    timestamp regression.

    The function does not modify the supplied records.
    """

    regression_indexes = set()

    if anomalies is not None:
        regression_indexes = {
            anomaly.record_index
            for anomaly in anomalies
            if anomaly.type == "timestamp_regression"
        }

    intervals = []

    previous_timestamp = None

    for index, record in enumerate(records):

        timestamp = record.timestamp

        if timestamp is None:
            continue

        if index in regression_indexes:
            previous_timestamp = timestamp
            continue

        if previous_timestamp is not None:
            intervals.append(timestamp - previous_timestamp)

        previous_timestamp = timestamp

    return intervals


def calculate_sampling_stats(
    intervals: list[timedelta],
) -> SamplingStats:
    """
    Calculate basic statistics for a collection of sampling intervals.

    The input list is not modified.
    """

    if not intervals:
        return SamplingStats(
            count=0,
            minimum=None,
            maximum=None,
            median=None,
            mode=None,
            dominant_count=0,
            dominant_percentage=None,
        )

    ordered = sorted(intervals)

    count = len(ordered)

    minimum = ordered[0]
    maximum = ordered[-1]

    middle = count // 2

    if count % 2 == 1:
        median = ordered[middle]
    else:
        median = (ordered[middle - 1] + ordered[middle]) / 2

    counter = Counter(ordered)

    mode, dominant_count = counter.most_common(1)[0]

    dominant_percentage = dominant_count / count * 100

    return SamplingStats(
        count=count,
        minimum=minimum,
        maximum=maximum,
        median=median,
        mode=mode,
        dominant_count=dominant_count,
        dominant_percentage=dominant_percentage,
    )


def count_sampling_intervals(
    intervals: list[timedelta],
) -> Counter[timedelta]:
    """
    Count the occurrences of each sampling interval.

    The input list is not modified.
    """

    return Counter(intervals)


def get_sampling_gap_context(
    records: list[History],
    index: int,
) -> tuple[History, History] | None:
    """
    Return the two history records that form a sampling interval.

    The index identifies the first record of the interval:

        records[index] -> records[index + 1]

    Returns None when the index does not identify a valid interval.

    The input list and records are not modified.
    """

    if index < 0:
        return None

    if index + 1 >= len(records):
        return None

    return records[index], records[index + 1]


def analyze_sampling_anomalies(
    records: list[History],
    expected_interval: timedelta | None = None,
    tolerance: timedelta = timedelta(seconds=10),
) -> list[dict]:
    """
    Analyze history records and identify sampling-related anomalies.

    Detects:

    - invalid_timestamp:
        A record has no timestamp.

    - timestamp_regression:
        A timestamp is earlier than the previous valid timestamp.

    - sampling_gap:
        The interval between two consecutive valid timestamps is
        approximately an integer multiple (> 1) of the expected interval.

    Timestamp regressions break the sampling sequence, so no sampling
    gap is calculated across a regression.

    The input records are not modified.
    """

    if expected_interval is not None:
        if expected_interval <= timedelta(0):
            raise ValueError("expected_interval must be greater than zero")

    if tolerance < timedelta(0):
        raise ValueError("tolerance must not be negative")

    anomalies = []

    previous_timestamp = None

    for index, record in enumerate(records):

        timestamp = record.timestamp

        # ---------------------------------------------------------
        # Invalid timestamp
        # ---------------------------------------------------------

        if timestamp is None:
            anomalies.append(
                {
                    "type": "invalid_timestamp",
                    "index": index,
                }
            )

            # An invalid timestamp cannot participate in the next
            # interval.
            previous_timestamp = None

            continue

        # ---------------------------------------------------------
        # Timestamp regression
        # ---------------------------------------------------------

        if previous_timestamp is not None and timestamp < previous_timestamp:
            anomalies.append(
                {
                    "type": "timestamp_regression",
                    "index": index,
                    "previous_timestamp": previous_timestamp,
                    "timestamp": timestamp,
                }
            )

            # A regression breaks the sampling sequence.
            previous_timestamp = timestamp

            continue

        # ---------------------------------------------------------
        # Sampling gap
        # ---------------------------------------------------------

        if expected_interval is not None and previous_timestamp is not None:
            interval = timestamp - previous_timestamp

            multiple = interval / expected_interval
            nearest_multiple = round(multiple)

            if (
                nearest_multiple >= 2
                and abs(interval - expected_interval * nearest_multiple) <= tolerance
            ):
                anomalies.append(
                    {
                        "type": "sampling_gap",
                        "index": index,
                        "interval": interval,
                        "expected_interval": expected_interval,
                        "multiple": nearest_multiple,
                    }
                )

        previous_timestamp = timestamp

    return anomalies
