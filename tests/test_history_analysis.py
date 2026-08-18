from datetime import datetime

from pyloninsight.analytics.history import (
    HistoryAnomaly,
    analyze_history,
)
from pyloninsight.models.history import History


def make_history(timestamp):
    return History(
        timestamp=timestamp,
        values={},
    )


def test_no_anomalies():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(datetime(2026, 6, 1, 10, 30, 0)),
        make_history(datetime(2026, 6, 1, 11, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert anomalies == []

    print("PASS: test_no_anomalies")


def test_timestamp_regression():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(datetime(2026, 6, 1, 10, 30, 0)),
        make_history(datetime(2026, 6, 1, 9, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert isinstance(anomaly, HistoryAnomaly)
    assert anomaly.type == "timestamp_regression"
    assert anomaly.record_index == 2
    assert anomaly.timestamp == datetime(2026, 6, 1, 9, 0, 0)
    assert anomaly.previous_timestamp == datetime(2026, 6, 1, 10, 30, 0)

    print("PASS: test_timestamp_regression")


def test_invalid_timestamp():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(None),
        make_history(datetime(2026, 6, 1, 11, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert isinstance(anomaly, HistoryAnomaly)
    assert anomaly.type == "invalid_timestamp"
    assert anomaly.record_index == 1
    assert anomaly.timestamp is None
    assert anomaly.previous_timestamp == datetime(2026, 6, 1, 10, 0, 0)

    print("PASS: test_invalid_timestamp")


def test_invalid_timestamp_does_not_break_regression_detection():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(None),
        make_history(datetime(2026, 6, 1, 9, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert len(anomalies) == 2

    assert anomalies[0].type == "invalid_timestamp"
    assert anomalies[0].record_index == 1

    assert anomalies[1].type == "timestamp_regression"
    assert anomalies[1].record_index == 2
    assert anomalies[1].timestamp == datetime(2026, 6, 1, 9, 0, 0)
    assert anomalies[1].previous_timestamp == datetime(2026, 6, 1, 10, 0, 0)

    print("PASS: " "test_invalid_timestamp_does_not_break_regression_detection")


def test_equal_timestamps_are_not_regression():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert anomalies == []

    print("PASS: test_equal_timestamps_are_not_regression")


def test_history_records_are_not_modified():
    timestamp_1 = datetime(2026, 6, 1, 10, 0, 0)
    timestamp_2 = datetime(2026, 6, 1, 9, 0, 0)

    records = [
        make_history(timestamp_1),
        make_history(timestamp_2),
    ]

    original_timestamps = [record.timestamp for record in records]

    analyze_history(records)

    assert [record.timestamp for record in records] == original_timestamps

    print("PASS: test_history_records_are_not_modified")


def test_anomaly_order():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
        make_history(datetime(2026, 6, 1, 9, 0, 0)),
        make_history(None),
        make_history(datetime(2026, 6, 1, 8, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert len(anomalies) == 3

    assert anomalies[0].record_index == 1
    assert anomalies[0].type == "timestamp_regression"

    assert anomalies[1].record_index == 2
    assert anomalies[1].type == "invalid_timestamp"

    assert anomalies[2].record_index == 3
    assert anomalies[2].type == "timestamp_regression"

    print("PASS: test_anomaly_order")


def test_empty_records():
    anomalies = analyze_history([])

    assert anomalies == []

    print("PASS: test_empty_records")


def test_single_record():
    records = [
        make_history(datetime(2026, 6, 1, 10, 0, 0)),
    ]

    anomalies = analyze_history(records)

    assert anomalies == []

    print("PASS: test_single_record")


def test_single_invalid_record():
    records = [
        make_history(None),
    ]

    anomalies = analyze_history(records)

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert anomaly.type == "invalid_timestamp"
    assert anomaly.record_index == 0
    assert anomaly.timestamp is None
    assert anomaly.previous_timestamp is None

    print("PASS: test_single_invalid_record")


def test(records=None):
    test_no_anomalies()
    test_timestamp_regression()
    test_invalid_timestamp()
    test_invalid_timestamp_does_not_break_regression_detection()
    test_equal_timestamps_are_not_regression()
    test_history_records_are_not_modified()
    test_anomaly_order()
    test_empty_records()
    test_single_record()
    test_single_invalid_record()


if __name__ == "__main__":
    test()
    print()
    print("10 tests passed.")
