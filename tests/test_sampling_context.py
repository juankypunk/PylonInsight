from datetime import datetime

from pyloninsight.analytics.sampling import get_sampling_gap_context
from pyloninsight.models.history import History


def make_record(timestamp, voltage):
    return History(
        timestamp=timestamp,
        values={
            "module_voltage": voltage,
        },
    )


def test_context_for_valid_index():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
        make_record(
            datetime(2026, 7, 1, 11, 0, 0),
            49800,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=1,
    )

    assert context is not None

    previous_record, current_record = context

    assert previous_record is records[1]
    assert current_record is records[2]

    assert previous_record.timestamp == datetime(2026, 7, 1, 10, 30, 0)
    assert current_record.timestamp == datetime(2026, 7, 1, 11, 0, 0)

    print("PASS: test_context_for_valid_index")


def test_first_interval():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=0,
    )

    assert context is not None

    previous_record, current_record = context

    assert previous_record is records[0]
    assert current_record is records[1]

    print("PASS: test_first_interval")


def test_last_record_has_no_following_interval():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=1,
    )

    assert context is None

    print("PASS: test_last_record_has_no_following_interval")


def test_negative_index_is_invalid():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=-1,
    )

    assert context is None

    print("PASS: test_negative_index_is_invalid")


def test_index_equal_to_length_is_invalid():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=len(records),
    )

    assert context is None

    print("PASS: test_index_equal_to_length_is_invalid")


def test_index_beyond_records_is_invalid():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=2,
    )

    assert context is None

    print("PASS: test_index_beyond_records_is_invalid")


def test_empty_records():
    context = get_sampling_gap_context(
        [],
        index=0,
    )

    assert context is None

    print("PASS: test_empty_records")


def test_single_record_has_no_interval():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
    ]

    context = get_sampling_gap_context(
        records,
        index=0,
    )

    assert context is None

    print("PASS: test_single_record_has_no_interval")


def test_records_are_not_modified():
    records = [
        make_record(
            datetime(2026, 7, 1, 10, 0, 0),
            50000,
        ),
        make_record(
            datetime(2026, 7, 1, 10, 30, 0),
            49900,
        ),
    ]

    original = list(records)

    context = get_sampling_gap_context(
        records,
        index=0,
    )

    assert context is not None
    assert records == original

    print("PASS: test_records_are_not_modified")


if __name__ == "__main__":
    test_context_for_valid_index()
    test_first_interval()
    test_last_record_has_no_following_interval()
    test_negative_index_is_invalid()
    test_index_equal_to_length_is_invalid()
    test_index_beyond_records_is_invalid()
    test_empty_records()
    test_single_record_has_no_interval()
    test_records_are_not_modified()

    print()
    print("9 tests passed.")
