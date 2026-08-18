from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.parsers.history_bmu import parse_bmu_history

DATA_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU1/history/"
    "UnknownSN_history_20260713203142.csv"
)


def test_bmu1_real_history():

    records = parse_bmu_history(DATA_FILE)

    anomalies = analyze_history(records)

    regressions = [
        anomaly for anomaly in anomalies if anomaly.type == "timestamp_regression"
    ]

    assert len(regressions) == 1

    anomaly = regressions[0]

    assert anomaly.timestamp.year == 2022
    assert anomaly.timestamp.month == 6
    assert anomaly.timestamp.day == 4

    assert anomaly.previous_timestamp.year == 2026
    assert anomaly.previous_timestamp.month == 6
    assert anomaly.previous_timestamp.day == 8

    print("PASS: test_bmu1_real_history")


if __name__ == "__main__":
    test_bmu1_real_history()

    print()
    print("1 test passed.")
