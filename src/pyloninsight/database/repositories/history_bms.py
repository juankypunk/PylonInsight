"""Repository for BMS history measurements."""

import logging
from datetime import datetime

import psycopg

from pyloninsight.models.history import History

logger = logging.getLogger(__name__)


class HistoryBMSRepository:
    """Persist BMS history measurements and their export associations.

    Measurements are uniquely identified by the physical device and
    timestamp. If a measurement already exists, its original values are
    preserved and the measurement is associated with the new export.
    """

    FIELD_MAPPING = (
        ("stack_voltage_mv", "stack_voltage"),
        ("stack_current_ma", "stack_current"),
        ("temperature_c", "temperature"),
        ("battery_temp_low_c", "battery_temp_low"),
        ("battery_temp_high_c", "battery_temp_high"),
        ("battery_voltage_low_mv", "battery_voltage_low"),
        ("battery_voltage_high_mv", "battery_voltage_high"),
        ("unit_temp_low_c", "unit_temp_low"),
        ("unit_temp_high_c", "unit_temp_high"),
        ("unit_voltage_low_mv", "unit_voltage_low"),
        ("unit_voltage_high_mv", "unit_voltage_high"),
        ("base_state", "base_state"),
        ("voltage_state", "voltage_state"),
        ("current_state", "current_state"),
        ("temperature_state", "temperature_state"),
        ("state_of_charge", "state_of_charge"),
        ("error_code", "error_code"),
        ("events", "events"),
        ("battery_events", "battery_events"),
        ("unit_events", "unit_events"),
    )

    DB_COLUMNS = tuple(column for column, _ in FIELD_MAPPING)

    VALUE_KEYS = tuple(key for _, key in FIELD_MAPPING)

    def __init__(self, connection: psycopg.Connection):
        """Initialize the repository with an existing database connection."""
        self.connection = connection

    def create_many(
        self,
        device_id: int,
        campaign_export_id: int,
        records: list[History],
    ) -> list[int]:
        """Persist measurements and associate them with a campaign export.

        Measurements are deduplicated by ``(device_id, timestamp)``.

        If a measurement already exists with different values, the existing
        measurement is preserved and a warning is logged.

        Records without a timestamp are skipped.

        Returns:
            The IDs of the persisted measurements, in input order, excluding
            records skipped because their timestamp is None.
        """
        if not records:
            return []

        valid_records = []

        for record in records:
            if record.timestamp is None:
                logger.warning(
                    "Skipping BMS history record without a timestamp "
                    "for device_id=%s and campaign_export_id=%s",
                    device_id,
                    campaign_export_id,
                )
                continue

            valid_records.append(record)

        if not valid_records:
            return []

        column_names = ", ".join(self.DB_COLUMNS)
        placeholders = ", ".join(["%s"] * (len(self.DB_COLUMNS) + 2))

        insert_sql = f"""
            INSERT INTO history_bms (
                device_id,
                record_timestamp,
                {column_names}
            )
            VALUES ({placeholders})
            ON CONFLICT (device_id, record_timestamp) DO NOTHING
            RETURNING id
        """

        select_sql = f"""
            SELECT id, {column_names}
            FROM history_bms
            WHERE device_id = %s
              AND record_timestamp = %s
        """

        association_sql = """
            INSERT INTO history_bms_export (
                history_bms_id,
                campaign_export_id
            )
            VALUES (%s, %s)
            ON CONFLICT (history_bms_id, campaign_export_id) DO NOTHING
        """

        history_ids = []

        with self.connection.cursor() as cursor:
            for record in valid_records:
                values = tuple(record.values[key] for key in self.VALUE_KEYS)

                cursor.execute(
                    insert_sql,
                    (
                        device_id,
                        record.timestamp,
                        *values,
                    ),
                )

                result = cursor.fetchone()

                if result is not None:
                    # A new measurement was inserted.
                    history_id = result[0]

                else:
                    # The measurement already exists for this device
                    # and timestamp. Retrieve its ID and stored values.
                    cursor.execute(
                        select_sql,
                        (device_id, record.timestamp),
                    )

                    existing = cursor.fetchone()

                    if existing is None:
                        # This should not normally happen: the preceding
                        # INSERT encountered a conflict on the unique key.
                        raise RuntimeError(
                            "BMS history measurement conflicted during "
                            "insertion but could not be retrieved "
                            f"(device_id={device_id}, "
                            f"timestamp={record.timestamp!s})"
                        )

                    history_id = existing[0]
                    stored_values = tuple(existing[1:])

                    if stored_values != values:
                        logger.warning(
                            "Conflicting BMS history values for "
                            "device_id=%s at timestamp=%s "
                            "(existing history_id=%s). "
                            "Keeping the existing measurement.",
                            device_id,
                            record.timestamp,
                            history_id,
                        )

                # Link the measurement to this export, whether it was
                # newly inserted or already existed.
                cursor.execute(
                    association_sql,
                    (history_id, campaign_export_id),
                )

                history_ids.append(history_id)

        self.connection.commit()

        return history_ids
