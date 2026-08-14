import csv
from datetime import datetime
from pathlib import Path

from pyloninsight.models.event import Event

CANONICAL_FIELDS = {
    "Vo(mV)": "module_voltage",
    "Tmpr": "module_temperature",
    "BTlow": "temperature_low",
    "BThigh": "temperature_high",
    "BVlow": "cell_voltage_low",
    "BVhigh": "cell_voltage_high",
    "PT.Tmpr": "positive_terminal_temperature",
    "NT.Tmpr": "negative_terminal_temperature",
    "Ref.Vol": "reference_voltage",
    "Fan.Pwm": "fan_pwm",
    "Fan1.Rpm": "fan1_rpm",
    "Fan2.Rpm": "fan2_rpm",
    "Base.St": "base_state",
    "Volt.St": "voltage_state",
    "Tmpr.St": "temperature_state",
    "PT.Tmpr.St": "positive_terminal_temperature_state",
    "NT.Tmpr.St": "negative_terminal_temperature_state",
    "Err.Code": "error_code",
    "Events": "events",
}


INTEGER_FIELDS = {
    "Vo(mV)",
    "Tmpr",
    "BTlow",
    "BThigh",
    "BVlow",
    "BVhigh",
    "PT.Tmpr",
    "NT.Tmpr",
    "Ref.Vol",
    "Fan.Pwm",
    "Fan1.Rpm",
    "Fan2.Rpm",
}


def parse_xhb_bmu_events(path: Path) -> list[Event]:
    """
    Parse a BatteryView event CSV file from an XHB_BMU_NT.

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

            if len(row) < 22:
                raise ValueError(
                    f"Unexpected number of fields: "
                    f"expected at least 22, got {len(row)}"
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
                "Tmpr",
                "BTlow",
                "BThigh",
                "BVlow",
                "BVhigh",
                "PT.Tmpr",
                "NT.Tmpr",
                "Ref.Vol",
                "Fan.Pwm",
                "Fan1.Rpm",
                "Fan2.Rpm",
                "Base.St",
                "Volt.St",
                "Tmpr.St",
                "PT.Tmpr.St",
                "NT.Tmpr.St",
                "Err.Code",
                "Events",
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
