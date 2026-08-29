from pathlib import Path

from pyloninsight.analytics.history import analyze_history
from pyloninsight.analytics.sampling import (
    calculate_sampling_intervals,
    calculate_sampling_stats,
    analyze_sampling_interval,
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

    for index, interval in enumerate(intervals):

        if interval == stats.mode:
            continue

        previous = records[index]
        current = records[index + 1]

        analysis = analyze_sampling_interval(
            previous,
            current,
            expected_interval=stats.mode,
        )

        print("-" * 60)
        print(f"Intervalo:       {analysis.interval}")
        print(f"Desviación:      {analysis.deviation}")

        print(f"Timestamp:       " f"{previous.timestamp} -> " f"{current.timestamp}")

        print(
            f"Module voltage:  "
            f"{analysis.module_voltage_before} -> "
            f"{analysis.module_voltage_after} "
            f"(Δ {analysis.module_voltage_delta})"
        )

        print(
            f"Module temp.:    "
            f"{analysis.module_temperature_before} -> "
            f"{analysis.module_temperature_after} "
            f"(Δ {analysis.module_temperature_delta})"
        )

        print(
            f"Voltage state:   "
            f"{analysis.voltage_state_before} -> "
            f"{analysis.voltage_state_after}"
        )

        print(
            f"Temperature state: "
            f"{analysis.temperature_state_before} -> "
            f"{analysis.temperature_state_after}"
        )

        print(
            f"Events:          "
            f"{analysis.events_before!r} -> "
            f"{analysis.events_after!r}"
        )

        print(
            f"Battery events:  "
            f"{analysis.battery_events_before!r} -> "
            f"{analysis.battery_events_after!r}"
        )

        if (
            analysis.battery_voltage_low_before is not None
            or analysis.battery_voltage_low_after is not None
        ):
            print(
                f"Battery V low:   "
                f"{analysis.battery_voltage_low_before} -> "
                f"{analysis.battery_voltage_low_after} "
                f"(Δ {analysis.battery_voltage_low_delta})"
            )

            print(
                f"Battery V high:  "
                f"{analysis.battery_voltage_high_before} -> "
                f"{analysis.battery_voltage_high_after} "
                f"(Δ {analysis.battery_voltage_high_delta})"
            )

            print(
                f"Battery T low:   "
                f"{analysis.battery_temp_low_before} -> "
                f"{analysis.battery_temp_low_after} "
                f"(Δ {analysis.battery_temp_low_delta})"
            )

            print(
                f"Battery T high:  "
                f"{analysis.battery_temp_high_before} -> "
                f"{analysis.battery_temp_high_after} "
                f"(Δ {analysis.battery_temp_high_delta})"
            )

            print(
                f"Error code:      "
                f"{analysis.error_code_before} -> "
                f"{analysis.error_code_after}"
            )


def test_bmu1_correlation():
    records = parse_bmu_history(BMU1_FILE)

    analyze_real_history(
        "BMU1",
        records,
    )

    print("PASS: test_bmu1_correlation")


def test_bmu3_correlation():
    records = parse_bmu_history(BMU3_FILE)

    analyze_real_history(
        "BMU3",
        records,
    )

    print("PASS: test_bmu3_correlation")


def test_bmu2_correlation():
    records = parse_xhb_bmu_history(BMU2_FILE)

    analyze_real_history(
        "BMU2 / XHB",
        records,
    )

    print("PASS: test_bmu2_correlation")


if __name__ == "__main__":
    test_bmu1_correlation()
    test_bmu3_correlation()
    test_bmu2_correlation()

    print()
    print("3 tests passed.")
