from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from pyloninsight.models.device import Device
from pyloninsight.models.device_snapshot import DeviceSnapshot

# Fields whose values have a well-defined representation in DeviceSnapshot.
_SNAPSHOT_FIELDS = {
    "board_version",
    "hardware_version",
    "firmware_version",
    "boot_version",
    "release_date",
    "cell_count",
    "capacity_ah",
    "nominal_voltage_v",
}


def parse_detailed(path: Path) -> tuple[Device, DeviceSnapshot]:
    """
    Parse a BatteryView detailed.txt file.

    The detailed file contains device identification and configuration
    information followed by diagnostic/statistical information.

    Only the device identification and configuration section is mapped
    to Device and DeviceSnapshot. Other fields are preserved in the
    snapshot's ``additional`` dictionary.

    Parameters
    ----------
    path:
        Path to the detailed.txt file.

    Returns
    -------
    tuple[Device, DeviceSnapshot]
        The device identity and the corresponding snapshot.

    Raises
    ------
    ValueError
        If no device name can be found.
    """

    metadata = _read_metadata(path)

    device_name = metadata.get("device_name")
    if not device_name:
        raise ValueError(f"Missing device name in detailed file: {path}")

    device = Device(
        barcode=metadata.get("module_barcode", ""),
        manufacturer=metadata.get("manufacturer"),
        model=device_name,
    )

    snapshot = DeviceSnapshot(
        board_version=metadata.get("board_version"),
        hardware_version=metadata.get("hardware_version"),
        firmware_version=metadata.get("soft_version"),
        boot_version=metadata.get("boot_version"),
        release_date=_parse_date(metadata.get("release_date")),
        cell_count=_parse_int(metadata.get("cell_number")),
        capacity_ah=_parse_capacity(metadata.get("specification")),
        nominal_voltage_v=_parse_voltage(metadata.get("specification")),
        additional={
            key: value for key, value in metadata.items() if key not in _SNAPSHOT_FIELDS
        },
    )

    return device, snapshot


def _read_metadata(path: Path) -> dict[str, str]:
    """
    Read key/value metadata from a BatteryView detailed file.

    Parsing stops when the diagnostic command section starts. This is
    currently identified by the first ``stat`` command prompt.

    Unknown fields are retained rather than discarded.
    """

    metadata: dict[str, str] = {}

    with path.open("r", encoding="utf-16-le") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line:
                continue

            if line == "stat":
                break

            if line in {"@", "$$", "pylon_debug>"}:
                continue

            if ":" not in line:
                continue

            raw_key, raw_value = line.split(":", 1)

            key = _normalize_key(raw_key)
            value = raw_value.strip()

            if not key:
                continue

            metadata[key] = value

    return metadata


def _normalize_key(key: str) -> str:
    """
    Convert a BatteryView detailed field name to a stable internal key.
    """

    normalized = " ".join(key.strip().split()).lower()

    mapping = {
        "device address": "device_address",
        "manufacturer": "manufacturer",
        "device name": "device_name",
        "board version": "board_version",
        "hard version": "hardware_version",
        "main soft version": "main_soft_version",
        "soft version": "soft_version",
        "sub soft version": "sub_soft_version",
        "boot version": "boot_version",
        "comm version": "comm_version",
        "release date": "release_date",
        "barcode": "barcode",
        "pcba barcode": "pcba_barcode",
        "module barcode": "module_barcode",
        "powersupply barcode": "powersupply_barcode",
        "power supply barcode": "powersupply_barcode",
        "device test time": "device_test_time",
        "specification": "specification",
        "cell number": "cell_number",
        "max dischg curr": "max_dischg_curr",
        "max charge curr": "max_charge_curr",
        "shut circuit": "shut_circuit",
        "relay feedback": "relay_feedback",
        "new board": "new_board",
        "fan exist": "fan_exist",
        "xhb_v3 board": "xhb_v3_board",
        "module afetype": "module_afetype",
        "module celltype": "module_celltype",
    }

    return mapping.get(normalized, normalized.replace(" ", "_"))


def _parse_date(value: str | None) -> date | None:
    """Parse a BatteryView date in YY-MM-DD format."""

    if not value:
        return None

    try:
        return datetime.strptime(value, "%y-%m-%d").date()
    except ValueError:
        return None


def _parse_int(value: str | None) -> int | None:
    """Parse an integer value."""

    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def _parse_capacity(specification: str | None) -> float | None:
    """
    Extract battery capacity in Ah from a specification such as
    ``48V/50AH`` or ``144V/50AH``.
    """

    if not specification:
        return None

    try:
        capacity = specification.upper().split("/", 1)[1]
        return float(capacity.removesuffix("AH").strip())
    except (IndexError, ValueError):
        return None


def _parse_voltage(specification: str | None) -> float | None:
    """
    Extract nominal voltage in V from a specification such as
    ``48V/50AH`` or ``144V/50AH``.
    """

    if not specification:
        return None

    try:
        voltage = specification.upper().split("/", 1)[0]
        return float(voltage.removesuffix("V").strip())
    except (IndexError, ValueError):
        return None
