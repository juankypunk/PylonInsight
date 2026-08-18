import csv
from datetime import datetime
from pathlib import Path

from pyloninsight.models.history import History

CANONICAL_FIELDS = {
    "Vo(mV)": "module_voltage",
    "Tempr": "module_temperature",
    "Tlow": "temperature_low",
    "Thigh": "temperature_high",
    "Vlowest": "cell_voltage_low",
    "Vhighest": "cell_voltage_high",
    "Volt.St": "voltage_state",
    "Temp.St": "temperature_state",
    "Events": "events",
    "BatEvents": "battery_events",
}


INTEGER_FIELDS = {
    "Vo(mV)",
    "Tempr",
    "Tlow",
    "Thigh",
    "Vlowest",
    "Vhighest",
}


def parse_bmu_history(path: Path) -> list[History]:
    """
    Parse a BatteryView history CSV file from a first-generation BMU.

    BatteryView stores Date and Time as two separate data fields,
    although the CSV header contains only "Time".
    """

    records = []

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.reader(file)

        # BatteryView header.
        next(reader)
        next(reader)
        next(reader)

        # CSV column header.
        next(reader)

        for row in reader:

            if not row:
                continue

            # BatteryView footer.
            if row[0] == "Command":
                break

            if row[0] == "$$":
                break  # Any non-numeric first field marks the end of the data.

            if not row[0].isdigit():
                break

            if len(row) < 12:
                raise ValueError(
                    f"Unexpected number of fields: "
                    f"expected at least 12, got {len(row)}"
                )

            record_date = row[1]
            record_time = row[2]

            timestamp = datetime.strptime(
                f"{record_date} {record_time}",
                "%y-%m-%d %H:%M:%S",
            )

            values = {}

            data_columns = [
                "Vo(mV)",
                "Tempr",
                "Tlow",
                "Thigh",
                "Vlowest",
                "Vhighest",
                "Volt.St",
                "Temp.St",
                "Events",
                "BatEvents",
            ]

            for index, column in enumerate(data_columns):

                value_index = index + 3

                if value_index >= len(row):
                    value = ""
                else:
                    value = row[value_index]

                canonical_name = CANONICAL_FIELDS[column]

                if column in INTEGER_FIELDS:
                    value = int(value)

                values[canonical_name] = value

            records.append(
                History(
                    timestamp=timestamp,
                    values=values,
                )
            )

    return records
