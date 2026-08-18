from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.parsers.history_xhb_bmu import parse_xhb_bmu_history

DATA_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU2/history/"
    "UnknownSN_history_20260713203417.csv"
)


def test_bmu2_real_history():
    records = parse_xhb_bmu_history(DATA_FILE)

    invalid_records = [record for record in records if record.timestamp is None]

    assert len(invalid_records) == 1

    invalid_record = invalid_records[0]

    assert invalid_record.timestamp is None

    anomalies = analyze_history(records)

    invalid_anomalies = [
        anomaly for anomaly in anomalies if anomaly.type == "invalid_timestamp"
    ]

    assert len(invalid_anomalies) == 1

    anomaly = invalid_anomalies[0]

    assert anomaly.timestamp is None

    print("PASS: test_bmu2_real_history")


if __name__ == "__main__":
    test_bmu2_real_history()

    print()
    print("1 test passed.")
