from datetime import timedelta

from pyloninsight.analytics.sampling import count_sampling_intervals


def test_count_sampling_intervals():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=30, seconds=1),
        timedelta(minutes=29, seconds=59),
        timedelta(minutes=30),
    ]

    distribution = count_sampling_intervals(intervals)

    assert distribution == {
        timedelta(minutes=30): 3,
        timedelta(minutes=30, seconds=1): 1,
        timedelta(minutes=29, seconds=59): 1,
    }

    print("PASS: test_count_sampling_intervals")


def test_empty_intervals():
    distribution = count_sampling_intervals([])

    assert distribution == {}

    print("PASS: test_empty_intervals")


def test_single_interval():
    intervals = [
        timedelta(minutes=7, seconds=30),
    ]

    distribution = count_sampling_intervals(intervals)

    assert distribution == {
        timedelta(minutes=7, seconds=30): 1,
    }

    print("PASS: test_single_interval")


def test_different_intervals():
    intervals = [
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=15),
        timedelta(minutes=7, seconds=30),
        timedelta(minutes=15, seconds=17),
        timedelta(minutes=7, seconds=30),
    ]

    distribution = count_sampling_intervals(intervals)

    assert distribution == {
        timedelta(minutes=7, seconds=30): 3,
        timedelta(minutes=15): 1,
        timedelta(minutes=15, seconds=17): 1,
    }

    print("PASS: test_different_intervals")


def test_input_intervals_are_not_modified():
    intervals = [
        timedelta(minutes=30),
        timedelta(minutes=30),
        timedelta(minutes=31),
    ]

    original = list(intervals)

    count_sampling_intervals(intervals)

    assert intervals == original

    print("PASS: test_input_intervals_are_not_modified")


if __name__ == "__main__":
    test_count_sampling_intervals()
    test_empty_intervals()
    test_single_interval()
    test_different_intervals()
    test_input_intervals_are_not_modified()

    print()
    print("5 tests passed.")
