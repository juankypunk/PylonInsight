from __future__ import annotations

import psycopg

from pyloninsight.models.device import Device


class DeviceRepository:
    """Persistence operations for Device objects."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create(self, device: Device) -> int:
        """Create a device and return its database ID."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO device (
                    barcode,
                    device_type,
                    manufacturer,
                    model,
                    specification,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    device.barcode,
                    device.device_type,
                    device.manufacturer,
                    device.model,
                    device.specification,
                    device.notes,
                ),
            )

            device_id = cursor.fetchone()[0]


        return device_id

    def get_by_barcode(self, barcode: str) -> Device | None:
        """Return a device by barcode, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    barcode,
                    device_type,
                    manufacturer,
                    model,
                    specification,
                    notes
                FROM device
                WHERE barcode = %s
                """,
                (barcode,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        (
            barcode,
            device_type,
            manufacturer,
            model,
            specification,
            notes,
        ) = row

        return Device(
            barcode=barcode,
            device_type=device_type,
            manufacturer=manufacturer,
            model=model,
            specification=specification,
            notes=notes,
        )

    def get_id_by_barcode(self, barcode: str) -> int | None:
        """Return the database ID of a device identified by its barcode."""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM device
                WHERE barcode = %s
                """,
                (barcode,),
            )
            result = cursor.fetchone()

        return result[0] if result is not None else None
