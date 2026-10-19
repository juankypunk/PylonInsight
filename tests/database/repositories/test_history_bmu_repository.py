"""Repository for BMU history measurements."""

import logging

import psycopg

from pyloninsight.models.history import History

logger = logging.getLogger(__name__)


class HistoryBMURepository:
    """Persist BMU history measurements and their export associations.

    Measurements are uniquely identified by the physical device and
    timestamp. If a measurement already exists, its original values are
    preserved and the measurement is associated with the new export.
    """

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
        """Persist measurements and associate them with a campaign export.

        Measurements are deduplicated by ``(device_id, record_timestamp)``.

        If an existing measurement has different values, its stored values
        are preserved and a warning is logged.

        Records without a timestamp are skipped.

        Returns:
            The IDs of the persisted measurements in input order, excluding
            records skipped because their timestamp is None.
        """
        if not records:
            return []

        valid_records = []

        for record in records:
            if record.timestamp is None:
                logger.warning(
                    "Skipping BMU history record without a timestamp "
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
            INSERT INTO history_bmu (
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
                    history_id = result[0]

                else:
                    cursor.execute(
                        select_sql,
                        (device_id, record.timestamp),
                    )

                    existing = cursor.fetchone()

                    if existing is None:
                        raise RuntimeError(
                            "BMU history measurement conflicted during "
                            "insertion but could not be retrieved "
                            f"(device_id={device_id}, "
                            f"timestamp={record.timestamp!s})"
                        )

                    history_id = existing[0]
                    stored_values = tuple(existing[1:])

                    if stored_values != values:
                        logger.warning(
                            "Conflicting BMU history values for "
                            "device_id=%s at timestamp=%s "
                            "(existing history_id=%s). "
                            "Keeping the existing measurement.",
                            device_id,
                            record.timestamp,
                            history_id,
                        )

                cursor.execute(
                    association_sql,
                    (history_id, campaign_export_id),
                )

                history_ids.append(history_id)

        self.connection.commit()

        return history_ids
