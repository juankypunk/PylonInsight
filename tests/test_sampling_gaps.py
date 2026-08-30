from datetime import timedelta

import pytest

from pyloninsight.analytics.sampling import find_sampling_gaps


def test_no_gaps():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert gaps == []

    print("PASS: test_no_gaps")


def test_one_missing_sample():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=60),
        timedelta(minutes=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert len(gaps) == 1

    gap = gaps[0]

    assert gap.index == 2
    assert gap.interval == timedelta(minutes=60)
    assert gap.expected_interval == timedelta(minutes=30)
    assert gap.multiple == 2

    print("PASS: test_one_missing_sample")


def test_two_missing_samples():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=90),
        timedelta(minutes=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert len(gaps) == 1

    gap = gaps[0]

    assert gap.index == 1
    assert gap.interval == timedelta(minutes=90)
    assert gap.expected_interval == timedelta(minutes=30)
    assert gap.multiple == 3

    print("PASS: test_two_missing_samples")


def test_small_jitter_is_not_gap():
    intervals = [
        timedelta(minutes=29, seconds=58),
        timedelta(minutes=30, seconds=1),
        timedelta(minutes=30),
        timedelta(minutes=30, seconds=2),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert gaps == []

    print("PASS: test_small_jitter_is_not_gap")


def test_non_multiple_interval_is_not_gap():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=31, seconds=17),
        timedelta(minutes=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert gaps == []

    print("PASS: test_non_multiple_interval_is_not_gap")


def test_zero_interval_is_not_gap():
    intervals = [
        timedelta(minutes=30),
        timedelta(0),
        timedelta(minutes=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert gaps == []

    print("PASS: test_zero_interval_is_not_gap")


def test_empty_intervals():
    gaps = find_sampling_gaps(
        [],
        expected_interval=timedelta(minutes=30),
    )

    assert gaps == []

    print("PASS: test_empty_intervals")


def test_input_intervals_are_not_modified():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=60),
        timedelta(minutes=30),
    ]

    original = list(intervals)

    find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
    )

    assert intervals == original

    print("PASS: test_input_intervals_are_not_modified")


def test_near_double_interval_is_gap():
    intervals = [
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=15, seconds=2),
        timedelta(minutes=7, seconds=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=7, seconds=30),
    )

    assert len(gaps) == 1

    gap = gaps[0]

    assert gap.index == 1
    assert gap.interval == timedelta(minutes=15, seconds=2)
    assert gap.expected_interval == timedelta(minutes=7, seconds=30)
    assert gap.multiple == 2

    print("PASS: test_near_double_interval_is_gap")


def test_far_from_double_interval_is_not_gap():
    intervals = [
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=15, seconds=17),
        timedelta(minutes=7, seconds=30),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=7, seconds=30),
    )

    assert gaps == []

    print("PASS: test_far_from_double_interval_is_not_gap")


def test_zero_expected_interval_raises():
    intervals = [
        timedelta(minutes=30),
    ]

    with pytest.raises(
        ValueError,
        match="expected_interval must be greater than zero",
    ):
        find_sampling_gaps(
            intervals,
            expected_interval=timedelta(0),
        )

    print("PASS: test_zero_expected_interval_raises")


def test_negative_expected_interval_raises():
    intervals = [
        timedelta(minutes=30),
    ]

    with pytest.raises(
        ValueError,
        match="expected_interval must be greater than zero",
    ):
        find_sampling_gaps(
            intervals,
            expected_interval=timedelta(minutes=-30),
        )

    print("PASS: test_negative_expected_interval_raises")


def test_negative_tolerance_raises():
    intervals = [
        timedelta(minutes=60),
    ]

    with pytest.raises(
        ValueError,
        match="tolerance must not be negative",
    ):
        find_sampling_gaps(
            intervals,
            expected_interval=timedelta(minutes=30),
            tolerance=timedelta(seconds=-1),
        )

    print("PASS: test_negative_tolerance_raises")


def test_gap_at_exact_tolerance_is_detected():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=60, seconds=10),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
        tolerance=timedelta(seconds=10),
    )

    assert len(gaps) == 1
    assert gaps[0].multiple == 2

    print("PASS: test_gap_at_exact_tolerance_is_detected")


def test_gap_beyond_tolerance_is_not_detected():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=60, seconds=11),
    ]

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=timedelta(minutes=30),
        tolerance=timedelta(seconds=10),
    )

    assert gaps == []

    print("PASS: test_gap_beyond_tolerance_is_not_detected")


if __name__ == "__main__":
    test_no_gaps()
    test_one_missing_sample()
    test_two_missing_samples()
    test_small_jitter_is_not_gap()
    test_non_multiple_interval_is_not_gap()
    test_zero_interval_is_not_gap()
    test_empty_intervals()
    test_input_intervals_are_not_modified()
    test_near_double_interval_is_gap()
    test_far_from_double_interval_is_not_gap()
    test_zero_expected_interval_raises()
    test_negative_expected_interval_raises()
    test_negative_tolerance_raises()
    test_gap_at_exact_tolerance_is_detected()
    test_gap_beyond_tolerance_is_not_detected()

    print()
    print("15 tests passed.")
