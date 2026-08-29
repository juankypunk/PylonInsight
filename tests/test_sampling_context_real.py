from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    calculate_sampling_intervals,
    calculate_sampling_stats,
    find_sampling_gaps,
    get_sampling_gap_context,
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


def analyze_real_history(name, records):
    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)
    print(f"Período esperado: {stats.mode}")
    print()

    # Buscar intervalos claramente superiores al período normal,
    # pero que no hayan sido clasificados como sampling gaps.
    suspicious = []

    for index, interval in enumerate(intervals):

        if interval > stats.mode:
            suspicious.append((index, interval))

    print(f"Intervalos superiores a la moda: " f"{len(suspicious)}")

    print()

    for index, interval in suspicious:

        context = get_sampling_gap_context(
            records,
            index,
        )

        if context is None:
            continue

        previous_record, current_record = context

        print("-" * 60)
        print(f"Intervalo {index}: {interval}")

        print(f"  anterior  [{index}]")
        print(f"    timestamp: {previous_record.timestamp}")
        print(f"    values:   {previous_record.values}")

        print(f"  siguiente [{index + 1}]")
        print(f"    timestamp: {current_record.timestamp}")
        print(f"    values:   {current_record.values}")


def test_bmu1_context():
    records = parse_bmu_history(BMU1_FILE)

    analyze_real_history(
        "BMU1",
        records,
    )

    print("PASS: test_bmu1_context")


def test_bmu3_context():
    records = parse_bmu_history(BMU3_FILE)

    analyze_real_history(
        "BMU3",
        records,
    )

    print("PASS: test_bmu3_context")


def test_bmu2_context():
    records = parse_xhb_bmu_history(BMU2_FILE)

    analyze_real_history(
        "BMU2 / XHB",
        records,
    )

    print("PASS: test_bmu2_context")


if __name__ == "__main__":
    test_bmu1_context()
    test_bmu3_context()
    test_bmu2_context()

    print()
    print("3 tests passed.")
