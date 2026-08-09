import csv
from datetime import datetime
from pathlib import Path

from pyloninsight.models.event import Event

CANONICAL_FIELDS = {
    "Vo(mV)": "stack_voltage",
    "Cu(mA)": "stack_current",
    "Tempr": "temperature",
    "BTlow": "battery_temp_low",
    "BThigh": "battery_temp_high",
    "BVlow": "battery_voltage_low",
    "BVhigh": "battery_voltage_high",
    "UTlow": "unit_temp_low",
    "UThigh": "unit_temp_high",
    "UVlow": "unit_voltage_low",
    "UVhigh": "unit_voltage_high",
    "Base.St": "base_state",
    "Volt.St": "voltage_state",
    "Curr.St": "current_state",
    "Temp.St": "temperature_state",
    "Per%": "state_of_charge",
    "ErrCode": "error_code",
    "Events": "events",
    "BatEvents": "battery_events",
    "UnitEvents": "unit_events",
}

INTEGER_FIELDS = {
    "stack_voltage",
    "stack_current",
    "temperature",
    "battery_temp_low",
    "battery_temp_high",
    "battery_voltage_low",
    "battery_voltage_high",
    "unit_temp_low",
    "unit_temp_high",
    "unit_voltage_low",
    "unit_voltage_high",
    "state_of_charge",
}


def parse_bms_events(path: Path) -> list[Event]:
    """
    Parse a BatteryView BMS event CSV file.

    BatteryView stores Date and Time as two separate data
    fields, although the CSV header contains only "Time":

        Item,Time,Vo(mV),Cu(mA),...

    Therefore the data columns are handled explicitly instead
    of matching the header and row using the same indexes.
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
        columns = next(reader)

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

            timestamp = datetime.strptime(
                f"{record_date} {record_time}",
                "%y-%m-%d %H:%M:%S",
            )

            values = {}

            # The first data fields are:
            #
            # row[0] = Item
            # row[1] = Date
            # row[2] = Time
            #
            # The CSV header has:
            #
            # columns[0] = Item
            # columns[1] = Time
            # columns[2] = Vo(mV)
            #
            # Therefore columns[2] corresponds to row[3].
            data_columns = [
                "Vo(mV)",
                "Cu(mA)",
                "Tempr",
                "BTlow",
                "BThigh",
                "BVlow",
                "BVhigh",
                "UTlow",
                "UThigh",
                "UVlow",
                "UVhigh",
                "Base.St",
                "Volt.St",
                "Curr.St",
                "Temp.St",
                "Per%",
                "ErrCode",
                "Events",
                "BatEvents",
                "UnitEvents",
            ]

            for index, column in enumerate(data_columns):

                value_index = index + 3

                if value_index >= len(row):
                    value = ""
                else:
                    value = row[value_index]

                canonical_name = CANONICAL_FIELDS[column]

                if canonical_name in INTEGER_FIELDS:
                    if canonical_name == "state_of_charge":
                        value = int(value.rstrip("%"))
                    else:
                        value = int(value)

                values[canonical_name] = value

            event_code = values.get("events", "")

            records.append(
                Event(
                    timestamp=timestamp,
                    event_code=event_code,
                    values=values,
                )
            )

    return records
