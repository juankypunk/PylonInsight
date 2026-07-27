from dataclasses import dataclass

from .base import BaseModel


@dataclass(slots=True)
class Device(BaseModel):
    """
    Physical Pylontech device.

    A Device represents a battery module or BMS identified by its
    barcode (serial number), independently of any acquisition campaign.
    """

    barcode: str

    manufacturer: str | None = None
    model: str | None = None

    notes: str | None = None