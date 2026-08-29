from datetime import timedelta
from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    calculate_sampling_intervals,
    calculate_sampling_stats,
    find_sampling_gaps,
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


def print_gaps(name, records, intervals, stats, gaps):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Período esperado:       {stats.mode}")
    print(f"Intervalos analizados:  {len(intervals)}")
    print(f"Gaps detectados:        {len(gaps)}")

    if not gaps:
        print("Ningún gap detectado.")
        return

    print()

    for gap in gaps:
        print(
            f"Gap en intervalo {gap.index}: "
            f"{gap.interval} "
            f"(x{gap.multiple}, "
            f"esperado {gap.expected_interval})"
        )

        interval_index = gap.index

        if interval_index >= len(records) - 1:
            continue

        previous_record = records[interval_index]
        current_record = records[interval_index + 1]

        print(
            f"    anterior: índice={interval_index} "
            f"timestamp={previous_record.timestamp}"
        )

        print(
            f"    siguiente: índice={interval_index + 1} "
            f"timestamp={current_record.timestamp}"
        )


def analyze_real_history(name, records):
    anomalies = analyze_history(records)

    intervals = calculate_sampling_intervals(
        records,
        anomalies=anomalies,
    )

    stats = calculate_sampling_stats(intervals)

    gaps = find_sampling_gaps(
        intervals,
        expected_interval=stats.mode,
    )

    print_gaps(
        name,
        records,
        intervals,
        stats,
        gaps,
    )

    return gaps


def test_bmu1_gaps():
    records = parse_bmu_history(BMU1_FILE)

    gaps = analyze_real_history(
        "BMU1",
        records,
    )

    print("PASS: test_bmu1_gaps")


def test_bmu3_gaps():
    records = parse_bmu_history(BMU3_FILE)

    gaps = analyze_real_history(
        "BMU3",
        records,
    )

    print("PASS: test_bmu3_gaps")


def test_bmu2_gaps():
    records = parse_xhb_bmu_history(BMU2_FILE)

    gaps = analyze_real_history(
        "BMU2 / XHB",
        records,
    )

    print("PASS: test_bmu2_gaps")


if __name__ == "__main__":
    test_bmu1_gaps()
    test_bmu3_gaps()
    test_bmu2_gaps()

    print()
    print("3 tests passed.")
