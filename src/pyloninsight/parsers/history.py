from pathlib import Path
from datetime import datetime
import csv

from pyloninsight.models.history import History

# BatteryView column names -> PylonInsight canonical names.
FIELD_MAP = {
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
}


def parse_bms_history(path: Path) -> list[History]:
    """
    Parse a BatteryView SC0500A BMS history CSV.
    """

    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))

    # Find the real column header.
    header_index = None

    for index, row in enumerate(rows):
        if row and row[0] == "Item":
            header_index = index
            break

    if header_index is None:
        raise ValueError("BMS history column header not found")

    column_header = rows[header_index]

    # BatteryView BMS exports omit Date from the column header,
    # although Date is present in every data record.
    if "Date" not in column_header:
        column_header = [
            "Item",
            "Date",
            *column_header[1:],
        ]

    records = []

    for row in rows[header_index + 1 :]:

        # Ignore empty lines and BatteryView footer.
        if not row:
            continue

        if row[0] in {"Command", "$$"}:
            continue

        # A valid data row must start with a numeric Item value.
        if not row[0].isdigit():
            continue

        # BatteryView may omit empty fields at the end of a record.
        # Complete the row with empty values so that it matches
        # the logical column structure.
        if len(row) < len(column_header):
            row = row + [""] * (len(column_header) - len(row))

        if len(row) > len(column_header):
            raise ValueError(
                f"Unexpected number of fields: "
                f"expected at most {len(column_header)}, got {len(row)}"
            )

        data = dict(zip(column_header, row))

        timestamp = datetime.strptime(
            f"{data['Date']} {data['Time']}",
            "%y-%m-%d %H:%M:%S",
        )

        values = {}

        for csv_name, canonical_name in FIELD_MAP.items():

            value = data[csv_name]

            if csv_name in INTEGER_FIELDS:
                value = int(value)

            elif csv_name == "Per%":
                value = int(value.rstrip("%"))

            values[canonical_name] = value

        records.append(
            History(
                timestamp=timestamp,
                values=values,
            )
        )

    return records
