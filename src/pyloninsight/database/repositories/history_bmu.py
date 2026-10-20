"""Repository for BMU history measurements."""

import logging

import psycopg

from pyloninsight.models.history import History

logger = logging.getLogger(__name__)


class HistoryBMURepository:
    """Persist BMU history measurements and their export associations."""

    FIELD_MAPPING = (
        ("module_voltage_mv", "module_voltage"),
        ("module_temperature_c", "module_temperature"),
        ("temperature_low_c", "temperature_low"),
        ("temperature_high_c", "temperature_high"),
        ("cell_voltage_low_mv", "cell_voltage_low"),
        ("cell_voltage_high_mv", "cell_voltage_high"),
        ("voltage_state", "voltage_state"),
        ("temperature_state", "temperature_state"),
        ("events", "events"),
        ("battery_events", "battery_events"),
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
        Insert BMU history measurements and associate them with an export.

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
                logger.warning("Skipping BMU history record without a timestamp")
                continue

            valid_records.append(record)

        if not valid_records:
            return []

        history_ids = []

        columns_sql = ", ".join(self.DB_COLUMNS)
        placeholders = ", ".join(["%s"] * (2 + len(self.DB_COLUMNS)))

        insert_sql = f"""
            INSERT INTO history_bmu (
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
            FROM history_bmu
            WHERE device_id = %s
              AND record_timestamp = %s
        """

        association_sql = """
            INSERT INTO history_bmu_export (
                history_bmu_id,
                campaign_export_id
            )
            VALUES (%s, %s)
            ON CONFLICT (history_bmu_id, campaign_export_id) DO NOTHING
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
                            "Could not retrieve existing BMU history "
                            f"measurement for device {device_id} at "
                            f"{record.timestamp}"
                        )

                    history_id = existing_row[0]
                    existing_values = tuple(existing_row[1:])

                    if existing_values != record_values:
                        logger.warning(
                            "Conflicting BMU history values for device "
                            "%s at %s. Keeping the existing measurement.",
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
