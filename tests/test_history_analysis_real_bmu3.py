from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.parsers.history_bmu import parse_bmu_history

DATA_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU3/history/"
    "UnknownSN_history_20260713203804.csv"
)


def test_bmu3_real_history():
    records = parse_bmu_history(DATA_FILE)

    anomalies = analyze_history(records)

    regressions = [
        anomaly for anomaly in anomalies if anomaly.type == "timestamp_regression"
    ]

    assert len(regressions) == 2

    first = regressions[0]

    assert first.timestamp is not None
    assert first.previous_timestamp is not None

    assert first.timestamp.strftime("%Y-%m-%d %H:%M:%S") == "2022-06-04 11:21:16"

    assert (
        first.previous_timestamp.strftime("%Y-%m-%d %H:%M:%S") == "2026-06-08 19:07:04"
    )

    second = regressions[1]

    assert second.timestamp is not None
    assert second.previous_timestamp is not None

    assert second.timestamp.strftime("%Y-%m-%d %H:%M:%S") == "2018-06-04 00:17:16"

    assert (
        second.previous_timestamp.strftime("%Y-%m-%d %H:%M:%S") == "2026-07-05 23:55:56"
    )

    print("PASS: test_bmu3_real_history")


if __name__ == "__main__":
    test_bmu3_real_history()

    print()
    print("1 test passed.")
