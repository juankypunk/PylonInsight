from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    calculate_sampling_intervals,
    calculate_sampling_stats,
    count_sampling_intervals,
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


def print_distribution(name, records, intervals):
    stats = calculate_sampling_stats(intervals)
    distribution = count_sampling_intervals(intervals)

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Intervalos:             {len(intervals)}")
    print(f"Moda:                   {stats.mode}")
    print(f"Mediana:                {stats.median}")
    print(f"Distintos:              {len(distribution)}")
    print()

    print("Intervalo                  Ocurrencias       %")
    print("-" * 55)

    for interval, count in sorted(
        distribution.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        percentage = count / len(intervals) * 100

        print(f"{str(interval):<25}" f"{count:>10}" f"{percentage:>12.2f}%")


def analyze_history_file(name, records):
    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    print_distribution(
        name,
        records,
        intervals,
    )


def test_bmu1_distribution():
    records = parse_bmu_history(BMU1_FILE)

    analyze_history_file(
        "BMU1",
        records,
    )

    print("PASS: test_bmu1_distribution")


def test_bmu3_distribution():
    records = parse_bmu_history(BMU3_FILE)

    analyze_history_file(
        "BMU3",
        records,
    )

    print("PASS: test_bmu3_distribution")


def test_bmu2_distribution():
    records = parse_xhb_bmu_history(BMU2_FILE)

    analyze_history_file(
        "BMU2 / XHB",
        records,
    )

    print("PASS: test_bmu2_distribution")


if __name__ == "__main__":
    test_bmu1_distribution()
    test_bmu3_distribution()
    test_bmu2_distribution()

    print()
    print("3 tests passed.")
