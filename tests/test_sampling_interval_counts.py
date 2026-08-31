from datetime import timedelta
from collections import Counter

from pyloninsight.analytics.sampling import count_sampling_intervals


def test_regular_intervals():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(minutes=30): 4,
        }
    )

    print("PASS: test_regular_intervals")


def test_different_intervals():
    intervals = [
        timedelta(minutes=15),
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=60),
        timedelta(minutes=30),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(minutes=15): 2,
            timedelta(minutes=30): 2,
            timedelta(minutes=60): 1,
        }
    )

    print("PASS: test_different_intervals")


def test_single_interval():
    intervals = [
        timedelta(minutes=30),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(minutes=30): 1,
        }
    )

    print("PASS: test_single_interval")


def test_empty_intervals():
    counts = count_sampling_intervals([])

    assert counts == Counter()

    print("PASS: test_empty_intervals")


def test_input_intervals_are_not_modified():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=30),
    ]

    original = list(intervals)

    count_sampling_intervals(intervals)

    assert intervals == original

    print("PASS: test_input_intervals_are_not_modified")


def test_zero_interval_is_counted():
    intervals = [
        timedelta(0),
        timedelta(minutes=30),
        timedelta(0),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(0): 2,
            timedelta(minutes=30): 1,
        }
    )

    print("PASS: test_zero_interval_is_counted")


def test_negative_interval_is_counted():
    intervals = [
        timedelta(minutes=-30),
        timedelta(minutes=30),
        timedelta(minutes=-30),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(minutes=-30): 2,
            timedelta(minutes=30): 1,
        }
    )

    print("PASS: test_negative_interval_is_counted")


def test_subsecond_precision_is_preserved():
    intervals = [
        timedelta(seconds=7, milliseconds=500),
        timedelta(seconds=7, milliseconds=500),
        timedelta(seconds=7, milliseconds=501),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(seconds=7, milliseconds=500): 2,
            timedelta(seconds=7, milliseconds=501): 1,
        }
    )

    print("PASS: test_subsecond_precision_is_preserved")


def test_tied_intervals_are_all_counted():
    intervals = [
        timedelta(minutes=15),
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=30),
    ]

    counts = count_sampling_intervals(intervals)

    assert counts == Counter(
        {
            timedelta(minutes=15): 2,
            timedelta(minutes=30): 2,
        }
    )

    print("PASS: test_tied_intervals_are_all_counted")


def test_result_is_counter():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    counts = count_sampling_intervals(intervals)

    assert isinstance(counts, Counter)

    print("PASS: test_result_is_counter")


if __name__ == "__main__":
    test_regular_intervals()
    test_different_intervals()
    test_single_interval()
    test_empty_intervals()
    test_input_intervals_are_not_modified()
    test_zero_interval_is_counted()
    test_negative_interval_is_counted()
    test_subsecond_precision_is_preserved()
    test_tied_intervals_are_all_counted()
    test_result_is_counter()

    print()
    print("10 tests passed.")
