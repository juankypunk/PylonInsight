from __future__ import annotations

import psycopg

from pyloninsight.models.event import Event


class EventBMURepository:
    """Persistence operations for BMU event records."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create_many(
        self,
        campaign_export_id: int,
        events: list[Event],
    ) -> list[int]:
        """Insert multiple BMU events and return their database IDs."""

        if not events:
            return []

        columns = (
            "campaign_export_id",
            "item",
            "record_timestamp",
            "module_voltage_mv",
            "module_temperature_c",
            "temperature_low_c",
            "temperature_high_c",
            "cell_voltage_low_mv",
            "cell_voltage_high_mv",
            "voltage_state",
            "temperature_state",
            "events",
            "battery_events",
        )

        placeholders = "(" + ", ".join(["%s"] * len(columns)) + ")"
        values_placeholders = ", ".join([placeholders] * len(events))

        query = f"""
            INSERT INTO event_bmu (
                {", ".join(columns)}
            )
            VALUES {values_placeholders}
            RETURNING id
        """

        parameters = []

        for event in events:
            values = event.values or {}

            parameters.extend(
                [
                    campaign_export_id,
                    event.item,
                    event.timestamp,
                    values["module_voltage"],
                    values["module_temperature"],
                    values["temperature_low"],
                    values["temperature_high"],
                    values["cell_voltage_low"],
                    values["cell_voltage_high"],
                    values["voltage_state"],
                    values["temperature_state"],
                    values["events"],
                    values["battery_events"],
                ]
            )

        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            event_ids = [row[0] for row in cursor.fetchall()]

        self.connection.commit()

        return event_ids

    def get_by_id(self, event_id: int) -> Event | None:
        """Return a BMU event by database ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    item,
                    record_timestamp,
                    module_voltage_mv,
                    module_temperature_c,
                    temperature_low_c,
                    temperature_high_c,
                    cell_voltage_low_mv,
                    cell_voltage_high_mv,
                    voltage_state,
                    temperature_state,
                    events,
                    battery_events
                FROM event_bmu
                WHERE id = %s
                """,
                (event_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        (
            item,
            timestamp,
            module_voltage,
            module_temperature,
            temperature_low,
            temperature_high,
            cell_voltage_low,
            cell_voltage_high,
            voltage_state,
            temperature_state,
            events,
            battery_events,
        ) = row

        values = {
            "module_voltage": module_voltage,
            "module_temperature": module_temperature,
            "temperature_low": temperature_low,
            "temperature_high": temperature_high,
            "cell_voltage_low": cell_voltage_low,
            "cell_voltage_high": cell_voltage_high,
            "voltage_state": voltage_state,
            "temperature_state": temperature_state,
            "events": events,
            "battery_events": battery_events,
        }

        return Event(
            item=item,
            timestamp=timestamp,
            event_code=battery_events,
            values=values,
        )
