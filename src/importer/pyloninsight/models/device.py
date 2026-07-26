from dataclasses import dataclass


@dataclass
class Device:
    """
    A physical Pylontech device.
    """

    barcode: str

    manufacturer: str | None = None
    model: str | None = None

    hardware_version: str | None = None
    firmware_version: str | None = None

    notes: str | None = None