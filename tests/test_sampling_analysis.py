from datetime import datetime, timedelta

from pyloninsight.analytics.sampling import calculate_sampling_intervals
from pyloninsight.models.history import History


def make_record(timestamp):
    return History(
        timestamp=timestamp,
        values={},
    )


def test_regular_intervals():
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

    print("PASS: test_regular_intervals")


def test_different_intervals_are_preserved():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 7, 30)),
        make_record(datetime(2026, 7, 1, 11, 7, 30)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=60),
    ]

    print("PASS: test_different_intervals_are_preserved")


def test_equal_timestamps_produce_zero_interval():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(0),
    ]

    print("PASS: test_equal_timestamps_produce_zero_interval")


def test_invalid_timestamp_is_skipped():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(None),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(hours=1),
    ]

    print("PASS: test_invalid_timestamp_is_skipped")


def test_invalid_timestamp_does_not_break_sequence():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
        make_record(None),
        make_record(datetime(2026, 7, 1, 10, 30, 0)),
        make_record(datetime(2026, 7, 1, 11, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == [
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    print("PASS: test_invalid_timestamp_does_not_break_sequence")


def test_records_are_not_modified():
    timestamp = datetime(2026, 7, 1, 10, 0, 0)

    records = [
        make_record(timestamp),
        make_record(timestamp + timedelta(minutes=30)),
    ]

    original = [record.timestamp for record in records]

    calculate_sampling_intervals(records)

    assert [record.timestamp for record in records] == original

    print("PASS: test_records_are_not_modified")


def test_empty_records():
    intervals = calculate_sampling_intervals([])

    assert intervals == []

    print("PASS: test_empty_records")


def test_single_record():
    records = [
        make_record(datetime(2026, 7, 1, 10, 0, 0)),
    ]

    intervals = calculate_sampling_intervals(records)

    assert intervals == []

    print("PASS: test_single_record")


if __name__ == "__main__":
    test_regular_intervals()
    test_different_intervals_are_preserved()
    test_equal_timestamps_produce_zero_interval()
    test_invalid_timestamp_is_skipped()
    test_invalid_timestamp_does_not_break_sequence()
    test_records_are_not_modified()
    test_empty_records()
    test_single_record()

    print()
    print("8 tests passed.")
