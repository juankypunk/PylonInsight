from datetime import datetime, timedelta

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    analyze_sampling_anomalies,
    calculate_sampling_intervals,
    calculate_sampling_stats,
)
from pyloninsight.models.history import History


def make_record(timestamp):
    return History(
        timestamp=timestamp,
        values={},
    )


def test_sampling_without_timestamp_regression():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    print("PASS: test_sampling_without_timestamp_regression")


def test_timestamp_regression_is_not_a_sampling_interval():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 9, 0, 0)),
        make_record(datetime(2026, 7, 1, 9, 30, 0)),
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
    ]

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    assert intervals == [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    print("PASS: test_timestamp_regression_is_not_a_sampling_interval")


def test_sampling_stats_ignore_timestamp_regression():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 9, 0, 0)),
        make_record(datetime(2026, 7, 1, 9, 30, 0)),
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
    ]

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 3
    assert stats.minimum == timedelta(minutes=30)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 3
    assert stats.dominant_percentage == 100.0

    print("PASS: test_sampling_stats_ignore_timestamp_regression")


def test_invalid_timestamp_is_not_a_sampling_interval():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(None),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    print("PASS: test_invalid_timestamp_is_not_a_sampling_interval")


def test_records_are_not_modified():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 9, 0, 0)),
    ]

    original = list(records)

    anomalies = analyze_history(records)

    calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    assert records == original

    print("PASS: test_records_are_not_modified")


def test_timestamp_regression_breaks_sampling_sequence():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 9, 0, 0)),
        make_record(datetime(2026, 7, 1, 9, 30, 0)),
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
    ]

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    assert intervals == [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    print("PASS: test_timestamp_regression_breaks_sampling_sequence")


def test_no_sampling_anomalies():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    result = analyze_sampling_anomalies(records)

    assert result == []

    print("PASS: test_no_sampling_anomalies")


def test_detect_timestamp_regression():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 9, 0, 0)),
    ]

    result = analyze_sampling_anomalies(records)

    assert len(result) == 1
    assert result[0]["type"] == "timestamp_regression"
    assert result[0]["index"] == 2

    print("PASS: test_detect_timestamp_regression")


def test_detect_invalid_timestamp():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(None),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    result = analyze_sampling_anomalies(records)

    assert len(result) == 1
    assert result[0]["type"] == "invalid_timestamp"
    assert result[0]["index"] == 1

    print("PASS: test_detect_invalid_timestamp")


def test_detect_sampling_gap():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 11, 30, 0)),
    ]

    result = analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
    )

    assert len(result) == 1
    assert result[0]["type"] == "sampling_gap"
    assert result[0]["index"] == 2
    assert result[0]["interval"] == timedelta(hours=1)

    print("PASS: test_detect_sampling_gap")


def test_sampling_anomalies_do_not_modify_records():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    original = list(records)

    analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
    )

    assert records == original

    print("PASS: test_sampling_anomalies_do_not_modify_records")


def test_sampling_gap_within_tolerance():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 9)),
    ]

    result = analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
        tolerance=timedelta(seconds=10),
    )

    assert len(result) == 1
    assert result[0]["type"] == "sampling_gap"
    assert result[0]["index"] == 1
    assert result[0]["interval"] == timedelta(minutes=60, seconds=9)
    assert result[0]["multiple"] == 2

    print("PASS: test_sampling_gap_within_tolerance")


def test_sampling_gap_outside_tolerance():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 11)),
    ]

    result = analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
        tolerance=timedelta(seconds=10),
    )

    assert result == []

    print("PASS: test_sampling_gap_outside_tolerance")


def test_non_multiple_interval_is_not_sampling_gap():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 45, 0)),
    ]

    result = analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
    )

    assert result == []

    print("PASS: test_non_multiple_interval_is_not_sampling_gap")


def test_sampling_gap_with_multiple_missing_samples():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 11, 30, 0)),
    ]

    result = analyze_sampling_anomalies(
        records,
        expected_interval=timedelta(minutes=30),
    )

    assert len(result) == 1
    assert result[0]["type"] == "sampling_gap"
    assert result[0]["index"] == 1
    assert result[0]["interval"] == timedelta(minutes=90)
    assert result[0]["expected_interval"] == timedelta(minutes=30)
    assert result[0]["multiple"] == 3

    print("PASS: test_sampling_gap_with_multiple_missing_samples")


def test_invalid_sampling_parameters():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
    ]

    try:
        analyze_sampling_anomalies(
            records,
            expected_interval=timedelta(0),
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "expected_interval must be greater than zero"

    try:
        analyze_sampling_anomalies(
            records,
            tolerance=timedelta(seconds=-1),
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "tolerance must not be negative"

    print("PASS: test_invalid_sampling_parameters")


if __name__ == "__main__":
    test_sampling_without_timestamp_regression()
    test_timestamp_regression_is_not_a_sampling_interval()
    test_sampling_stats_ignore_timestamp_regression()
    test_invalid_timestamp_is_not_a_sampling_interval()
    test_records_are_not_modified()
    test_timestamp_regression_breaks_sampling_sequence()
    test_no_sampling_anomalies()
    test_detect_timestamp_regression()
    test_detect_invalid_timestamp()
    test_detect_sampling_gap()
    test_sampling_anomalies_do_not_modify_records()
    test_sampling_gap_within_tolerance()
    test_sampling_gap_outside_tolerance()
    test_non_multiple_interval_is_not_sampling_gap()
    test_sampling_gap_with_multiple_missing_samples()
    test_invalid_sampling_parameters()

    print()
    print("16 tests passed.")
