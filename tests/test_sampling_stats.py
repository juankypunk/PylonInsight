import pytest
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


def test_mode_with_tied_intervals():
    intervals = [
        timedelta(minutes=15),
        timedelta(minutes=30),
        timedelta(minutes=15),
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 4
    assert stats.minimum == timedelta(minutes=15)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=22, seconds=30)

    assert stats.mode == timedelta(minutes=15)
    assert stats.dominant_count == 2
    assert stats.dominant_percentage == 50.0

    print("PASS: test_mode_with_tied_intervals")


def test_all_intervals_are_different():
    intervals = [
        timedelta(minutes=10),
        timedelta(minutes=20),
        timedelta(minutes=30),
        timedelta(minutes=40),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 4
    assert stats.minimum == timedelta(minutes=10)
    assert stats.maximum == timedelta(minutes=40)
    assert stats.median == timedelta(minutes=25)

    assert stats.dominant_count == 1
    assert stats.dominant_percentage == 25.0

    print("PASS: test_all_intervals_are_different")


def test_median_preserves_subsecond_precision():
    intervals = [
        timedelta(seconds=1),
        timedelta(seconds=2),
        timedelta(seconds=3),
        timedelta(seconds=4),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.median == timedelta(seconds=2, microseconds=500000)

    print("PASS: test_median_preserves_subsecond_precision")


def test_zero_interval_is_valid_statistical_value():
    intervals = [
        timedelta(0),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 3
    assert stats.minimum == timedelta(0)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 2
    assert stats.dominant_percentage == pytest.approx(200 / 3)

    print("PASS: test_zero_interval_is_valid_statistical_value")


def test_negative_intervals_are_processed_as_values():
    intervals = [
        timedelta(minutes=-30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    stats = calculate_sampling_stats(intervals)

    assert stats.count == 3
    assert stats.minimum == timedelta(minutes=-30)
    assert stats.maximum == timedelta(minutes=30)
    assert stats.median == timedelta(minutes=30)
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count == 2
    assert stats.dominant_percentage == pytest.approx(200 / 3)

    print("PASS: test_negative_intervals_are_processed_as_values")


if __name__ == "__main__":
    test_regular_sampling()
    test_different_intervals()
    test_mode_is_most_frequent_interval()
    test_empty_intervals()
    test_single_interval()
    test_input_intervals_are_not_modified()
    test_median_with_even_number_of_intervals()
    test_median_with_odd_number_of_intervals()
    test_mode_with_tied_intervals()
    test_all_intervals_are_different()
    test_median_preserves_subsecond_precision()
    test_zero_interval_is_valid_statistical_value()
    test_negative_intervals_are_processed_as_values()

    print()
    print("13 tests passed.")
