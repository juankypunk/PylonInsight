from pathlib import Path
from datetime import timedelta

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    calculate_sampling_intervals,
    calculate_sampling_stats,
)
from pyloninsight.parsers.history_bmu import parse_bmu_history
from pyloninsight.parsers.history_xhb_bmu import parse_xhb_bmu_history

BMU1_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU1/history/"
    "UnknownSN_history_20260713203142.csv"
)

BMU3_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU3/history/"
    "UnknownSN_history_20260713203804.csv"
)

BMU2_FILE = Path(
    "tests/data/real/"
    "2026-07-13_SOC100/"
    "BMU2/history/"
    "UnknownSN_history_20260713203417.csv"
)


def print_stats(name, stats, anomalies):
    regression_count = sum(
        1 for anomaly in anomalies if anomaly.type == "timestamp_regression"
    )

    invalid_count = sum(
        1 for anomaly in anomalies if anomaly.type == "invalid_timestamp"
    )

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Regresiones temporales:  {regression_count}")
    print(f"Timestamp inválidos:     {invalid_count}")
    print(f"Intervalos válidos:      {stats.count}")
    print(f"Mínimo:                  {stats.minimum}")
    print(f"Máximo:                  {stats.maximum}")
    print(f"Mediana:                 {stats.median}")
    print(f"Moda:                    {stats.mode}")
    print(f"Ocurrencias de la moda:  {stats.dominant_count}")
    print(f"Porcentaje de la moda:   {stats.dominant_percentage:.2f}%")


def test_bmu1_sampling():
    records = parse_bmu_history(BMU1_FILE)

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    assert stats.count > 0
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count > 0
    assert stats.dominant_percentage > 0

    print_stats("BMU1", stats, anomalies)

    print("PASS: test_bmu1_sampling")


def test_bmu3_sampling():
    records = parse_bmu_history(BMU3_FILE)

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    assert stats.count > 0
    assert stats.mode == timedelta(minutes=30)
    assert stats.dominant_count > 0
    assert stats.dominant_percentage > 0

    print_stats("BMU3", stats, anomalies)

    print("PASS: test_bmu3_sampling")


def test_bmu2_sampling():
    records = parse_xhb_bmu_history(BMU2_FILE)

    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    assert stats.count > 0
    assert stats.mode == timedelta(minutes=7, seconds=30)
    assert stats.dominant_count > 0
    assert stats.dominant_percentage > 0

    print_stats("BMU2 / XHB", stats, anomalies)

    print("PASS: test_bmu2_sampling")


if __name__ == "__main__":
    test_bmu1_sampling()
    test_bmu3_sampling()
    test_bmu2_sampling()

    print()
    print("3 tests passed.")
