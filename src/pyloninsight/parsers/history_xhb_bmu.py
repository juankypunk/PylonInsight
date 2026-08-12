import csv
from datetime import datetime
from pathlib import Path

from pyloninsight.models.history import History

CANONICAL_FIELDS = {
    "Vo(mV)": "module_voltage",
    "Tmpr": "module_temperature",
    "BTlow": "battery_temp_low",
    "BThigh": "battery_temp_high",
    "BVlow": "battery_voltage_low",
    "BVhigh": "battery_voltage_high",
    "PT.Tmpr": "positive_temperature",
    "NT.Tmpr": "negative_temperature",
    "Ref.Vol": "reference_voltage",
    "Fan.Pwm": "fan_pwm",
    "Fan1.Rpm": "fan1_rpm",
    "Fan2.Rpm": "fan2_rpm",
    "Base.St": "base_state",
    "Volt.St": "voltage_state",
    "Tmpr.St": "temperature_state",
    "PT.Tmpr.St": "positive_temperature_state",
    "NT.Tmpr.St": "negative_temperature_state",
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


def parse_xhb_bmu_history(path: Path) -> list[History]:
    """
    Parse a BatteryView history CSV file from an XHB_BMU_NT.

    BatteryView stores Date and Time as two separate data fields,
    although the CSV header contains only "Time".

    Invalid timestamps such as:

        00-00-00,00:00:00

    are preserved as None instead of causing the parser to fail.
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
                break

            if len(row) < 21:
                raise ValueError(
                    f"Unexpected number of fields: "
                    f"expected at least 21, got {len(row)}"
                )

            record_date = row[1]
            record_time = row[2]

            try:
                timestamp = datetime.strptime(
                    f"{record_date} {record_time}",
                    "%y-%m-%d %H:%M:%S",
                )
            except ValueError:
                timestamp = None

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
