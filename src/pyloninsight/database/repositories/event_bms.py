from __future__ import annotations

import psycopg

from pyloninsight.models.event import Event


class EventBMSRepository:
    """Persistence operations for BMS event records."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create_many(
        self,
        campaign_export_id: int,
        events: list[Event],
    ) -> list[int]:
        """Insert multiple BMS events and return their database IDs."""

        if not events:
            return []

        columns = (
            "campaign_export_id",
            "item",
            "record_timestamp",
            "stack_voltage_mv",
            "stack_current_ma",
            "temperature_c",
            "battery_temp_low_c",
            "battery_temp_high_c",
            "battery_voltage_low_mv",
            "battery_voltage_high_mv",
            "unit_temp_low_c",
            "unit_temp_high_c",
            "unit_voltage_low_mv",
            "unit_voltage_high_mv",
            "base_state",
            "voltage_state",
            "current_state",
            "temperature_state",
            "state_of_charge",
            "error_code",
            "events",
            "battery_events",
            "unit_events",
        )

        placeholders = "(" + ", ".join(["%s"] * len(columns)) + ")"
        values_placeholders = ", ".join([placeholders] * len(events))

        query = f"""
            INSERT INTO event_bms (
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
                    values["stack_voltage"],
                    values["stack_current"],
                    values["temperature"],
                    values["battery_temp_low"],
                    values["battery_temp_high"],
                    values["battery_voltage_low"],
                    values["battery_voltage_high"],
                    values["unit_temp_low"],
                    values["unit_temp_high"],
                    values["unit_voltage_low"],
                    values["unit_voltage_high"],
                    values["base_state"],
                    values["voltage_state"],
                    values["current_state"],
                    values["temperature_state"],
                    values["state_of_charge"],
                    values["error_code"],
                    values["events"],
                    values["battery_events"],
                    values["unit_events"],
                ]
            )

        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            event_ids = [row[0] for row in cursor.fetchall()]


        return event_ids

    def get_by_id(self, event_id: int) -> Event | None:
        """Return a BMS event by database ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    item,
                    record_timestamp,
                    stack_voltage_mv,
                    stack_current_ma,
                    temperature_c,
                    battery_temp_low_c,
                    battery_temp_high_c,
                    battery_voltage_low_mv,
                    battery_voltage_high_mv,
                    unit_temp_low_c,
                    unit_temp_high_c,
                    unit_voltage_low_mv,
                    unit_voltage_high_mv,
                    base_state,
                    voltage_state,
                    current_state,
                    temperature_state,
                    state_of_charge,
                    error_code,
                    events,
                    battery_events,
                    unit_events
                FROM event_bms
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
            stack_voltage,
            stack_current,
            temperature,
            battery_temp_low,
            battery_temp_high,
            battery_voltage_low,
            battery_voltage_high,
            unit_temp_low,
            unit_temp_high,
            unit_voltage_low,
            unit_voltage_high,
            base_state,
            voltage_state,
            current_state,
            temperature_state,
            state_of_charge,
            error_code,
            events,
            battery_events,
            unit_events,
        ) = row

        values = {
            "stack_voltage": stack_voltage,
            "stack_current": stack_current,
            "temperature": temperature,
            "battery_temp_low": battery_temp_low,
            "battery_temp_high": battery_temp_high,
            "battery_voltage_low": battery_voltage_low,
            "battery_voltage_high": battery_voltage_high,
            "unit_temp_low": unit_temp_low,
            "unit_temp_high": unit_temp_high,
            "unit_voltage_low": unit_voltage_low,
            "unit_voltage_high": unit_voltage_high,
            "base_state": base_state,
            "voltage_state": voltage_state,
            "current_state": current_state,
            "temperature_state": temperature_state,
            "state_of_charge": state_of_charge,
            "error_code": error_code,
            "events": events,
            "battery_events": battery_events,
            "unit_events": unit_events,
        }

        return Event(
            item=item,
            timestamp=timestamp,
            event_code=events,
            values=values,
        )
