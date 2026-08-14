import csv
from datetime import datetime
from pathlib import Path

from pyloninsight.models.event import Event

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


def parse_bmu_events(path: Path) -> list[Event]:
    """
    Parse a BatteryView event CSV file from a first-generation BMU.

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

        # CSV column header.
        next(reader)

        for row in reader:

            if not row:
                continue

            # BatteryView footer.
            if row[0] == "Command":
                break

            if row[0] == "$$":
                break

            if len(row) < 13:
                raise ValueError(
                    f"Unexpected number of fields: "
                    f"expected at least 13, got {len(row)}"
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
                    value = row[value_index].strip()

                canonical_name = CANONICAL_FIELDS[column]

                if column in INTEGER_FIELDS:
                    value = int(value)

                values[canonical_name] = value

            event_code = values["events"]

            records.append(
                Event(
                    timestamp=timestamp,
                    event_code=event_code,
                    values=values,
                )
            )

    return records
