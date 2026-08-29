from datetime import timedelta

from pyloninsight.analytics.sampling import calculate_sampling_stats
from pyloninsight.models.history import History


def make_record(timestamp):
    return History(
        timestamp=timestamp,
        values={},
    )


def test_regular_sampling():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 4
    assert stats.minimum == timedelta(minutes=30)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 4
    assert stats.dominant_percentage == 100.0

    print("PASS: test_regular_sampling")


def test_different_intervals():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=30),
        timedelta(minutes=60),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 5
    assert stats.minimum == timedelta(minutes=15)
    assert stats.maximum == timedelta(minutes=60)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 3
    assert stats.dominant_percentage == 60.0

    print("PASS: test_different_intervals")


def test_mode_is_most_frequent_interval():
    intervals = [
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=15),
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.mode == timedelta(minutes=7, seconds=30)
    assert stats.dominant_count == 3
    assert stats.dominant_percentage == 60.0

    print("PASS: test_mode_is_most_frequent_interval")


def test_empty_intervals():
    stats = calculate_sampling_stats([])

    assert stats.count == 0
    assert stats.minimum is None
    assert stats.maximum is None
    assert stats.median is None
    assert stats.mode is None
    assert stats.dominant_count == 0
    assert stats.dominant_percentage is None

    print("PASS: test_empty_intervals")


def test_single_interval():
    intervals = [
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 1
    assert stats.minimum == timedelta(minutes=30)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 1
    assert stats.dominant_percentage == 100.0

    print("PASS: test_single_interval")


def test_input_intervals_are_not_modified():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=60),
    ]

    original = list(intervals)

    calculate_sampling_stats(intervals)

    assert intervals == original

    print("PASS: test_input_intervals_are_not_modified")


def test_median_with_even_number_of_intervals():
    intervals = [
        timedelta(minutes=10),
        timedelta(minutes=20),
        timedelta(minutes=30),
        timedelta(minutes=40),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.median == timedelta(minutes=25)

    print("PASS: test_median_with_even_number_of_intervals")


def test_median_with_odd_number_of_intervals():
    intervals = [
        timedelta(minutes=10),
        timedelta(minutes=20),
        timedelta(minutes=90),
        timedelta(minutes=30),
        timedelta(minutes=40),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.median == timedelta(minutes=30)

    print("PASS: test_median_with_odd_number_of_intervals")


if __name__ == "__main__":
    test_regular_sampling()
    test_different_intervals()
    test_mode_is_most_frequent_interval()
    test_empty_intervals()
    test_single_interval()
    test_input_intervals_are_not_modified()
    test_median_with_even_number_of_intervals()
    test_median_with_odd_number_of_intervals()

    print()
    print("8 tests passed.")
