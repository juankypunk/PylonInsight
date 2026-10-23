from __future__ import annotations

import psycopg

from pyloninsight.models.event import Event


class EventXHBMURepository:
    """Persistence operations for XHB BMU event records."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create_many(
        self,
        campaign_export_id: int,
        events: list[Event],
    ) -> list[int]:
        """Insert multiple XHB BMU events and return their database IDs."""

        if not events:
            return []

        columns = (
            "campaign_export_id",
            "item",
            "record_timestamp",
            "module_voltage_mv",
            "module_temperature_c",
            "battery_temperature_low_c",
            "battery_temperature_high_c",
            "cell_voltage_low_mv",
            "cell_voltage_high_mv",
            "positive_terminal_temperature_c",
            "negative_terminal_temperature_c",
            "reference_voltage_mv",
            "fan_pwm",
            "fan1_rpm",
            "fan2_rpm",
            "base_state",
            "voltage_state",
            "temperature_state",
            "positive_terminal_temperature_state",
            "negative_terminal_temperature_state",
            "error_code",
            "events",
        )

        placeholders = "(" + ", ".join(["%s"] * len(columns)) + ")"
        values_placeholders = ", ".join([placeholders] * len(events))

        query = f"""
            INSERT INTO event_xhb_bmu (
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
                    values["positive_terminal_temperature"],
                    values["negative_terminal_temperature"],
                    values["reference_voltage"],
                    values["fan_pwm"],
                    values["fan1_rpm"],
                    values["fan2_rpm"],
                    values["base_state"],
                    values["voltage_state"],
                    values["temperature_state"],
                    values["positive_terminal_temperature_state"],
                    values["negative_terminal_temperature_state"],
                    values["error_code"],
                    values["events"],
                ]
            )

        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            event_ids = [row[0] for row in cursor.fetchall()]


        return event_ids

    def get_by_id(self, event_id: int) -> Event | None:
        """Return an XHB BMU event by ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    item,
                    record_timestamp,
                    module_voltage_mv,
                    module_temperature_c,
                    battery_temperature_low_c,
                    battery_temperature_high_c,
                    cell_voltage_low_mv,
                    cell_voltage_high_mv,
                    positive_terminal_temperature_c,
                    negative_terminal_temperature_c,
                    reference_voltage_mv,
                    fan_pwm,
                    fan1_rpm,
                    fan2_rpm,
                    base_state,
                    voltage_state,
                    temperature_state,
                    positive_terminal_temperature_state,
                    negative_terminal_temperature_state,
                    error_code,
                    events
                FROM event_xhb_bmu
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
            positive_terminal_temperature,
            negative_terminal_temperature,
            reference_voltage,
            fan_pwm,
            fan1_rpm,
            fan2_rpm,
            base_state,
            voltage_state,
            temperature_state,
            positive_terminal_temperature_state,
            negative_terminal_temperature_state,
            error_code,
            events,
        ) = row

        values = {
            "module_voltage": module_voltage,
            "module_temperature": module_temperature,
            "temperature_low": temperature_low,
            "temperature_high": temperature_high,
            "cell_voltage_low": cell_voltage_low,
            "cell_voltage_high": cell_voltage_high,
            "positive_terminal_temperature": positive_terminal_temperature,
            "negative_terminal_temperature": negative_terminal_temperature,
            "reference_voltage": reference_voltage,
            "fan_pwm": fan_pwm,
            "fan1_rpm": fan1_rpm,
            "fan2_rpm": fan2_rpm,
            "base_state": base_state,
            "voltage_state": voltage_state,
            "temperature_state": temperature_state,
            "positive_terminal_temperature_state": (
                positive_terminal_temperature_state
            ),
            "negative_terminal_temperature_state": (
                negative_terminal_temperature_state
            ),
            "error_code": error_code,
            "events": events,
        }

        return Event(
            item=item,
            timestamp=timestamp,
            event_code=events,
            values=values,
        )
