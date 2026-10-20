"""Repository for XHB_BMU_NT history measurements."""

import logging

import psycopg

from pyloninsight.models.history import History

logger = logging.getLogger(__name__)


class HistoryXHBBMURepository:
    """Persist XHB_BMU_NT history measurements and export associations."""

    FIELD_MAPPING = (
        ("module_voltage_mv", "module_voltage"),
        ("module_temperature_c", "module_temperature"),
        ("battery_temperature_low_c", "battery_temp_low"),
        ("battery_temperature_high_c", "battery_temp_high"),
        ("cell_voltage_low_mv", "battery_voltage_low"),
        ("cell_voltage_high_mv", "battery_voltage_high"),
        ("positive_terminal_temperature_c", "positive_terminal_temperature"),
        ("negative_terminal_temperature_c", "negative_terminal_temperature"),
        ("reference_voltage_mv", "reference_voltage"),
        ("fan_pwm", "fan_pwm"),
        ("fan1_rpm", "fan1_rpm"),
        ("fan2_rpm", "fan2_rpm"),
        ("base_state", "base_state"),
        ("voltage_state", "voltage_state"),
        ("temperature_state", "temperature_state"),
        (
            "positive_terminal_temperature_state",
            "positive_terminal_temperature_state",
        ),
        (
            "negative_terminal_temperature_state",
            "negative_terminal_temperature_state",
        ),
        ("error_code", "error_code"),
        ("events", "events"),
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
        """
        Insert measurements and associate them with an export.

        Measurements are uniquely identified by device and timestamp.
        Existing measurements are reused rather than overwritten.

        Returns:
            The database IDs of the measurements processed.
        """
        if not records:
            return []

        valid_records = []

        for record in records:
            if record.timestamp is None:
                logger.warning("Skipping XHB_BMU_NT history record without a timestamp")
                continue

            valid_records.append(record)

        if not valid_records:
            return []

        history_ids = []

        columns_sql = ", ".join(self.DB_COLUMNS)
        placeholders = ", ".join(["%s"] * (2 + len(self.DB_COLUMNS)))

        insert_sql = f"""
            INSERT INTO history_xhb_bmu (
                device_id,
                record_timestamp,
                {columns_sql}
            )
            VALUES ({placeholders})
            ON CONFLICT (device_id, record_timestamp) DO NOTHING
            RETURNING id
        """

        select_sql = f"""
            SELECT id, {columns_sql}
            FROM history_xhb_bmu
            WHERE device_id = %s
              AND record_timestamp = %s
        """

        association_sql = """
            INSERT INTO history_xhb_bmu_export (
                history_xhb_bmu_id,
                campaign_export_id
            )
            VALUES (%s, %s)
            ON CONFLICT (history_xhb_bmu_id, campaign_export_id) DO NOTHING
        """

        with self.connection.cursor() as cursor:
            for record in valid_records:
                record_values = tuple(record.values[key] for key in self.VALUE_KEYS)

                cursor.execute(
                    insert_sql,
                    (
                        device_id,
                        record.timestamp,
                        *record_values,
                    ),
                )

                row = cursor.fetchone()

                if row is not None:
                    history_id = row[0]
                else:
                    cursor.execute(
                        select_sql,
                        (device_id, record.timestamp),
                    )

                    existing_row = cursor.fetchone()

                    if existing_row is None:
                        raise RuntimeError(
                            "Could not retrieve existing XHB_BMU_NT history "
                            f"measurement for device {device_id} at "
                            f"{record.timestamp}"
                        )

                    history_id = existing_row[0]
                    existing_values = tuple(existing_row[1:])

                    if existing_values != record_values:
                        logger.warning(
                            "Conflicting XHB_BMU_NT history values for "
                            "device %s at %s. Keeping the existing measurement.",
                            device_id,
                            record.timestamp,
                        )

                cursor.execute(
                    association_sql,
                    (history_id, campaign_export_id),
                )

                history_ids.append(history_id)

        self.connection.commit()

        return history_ids
