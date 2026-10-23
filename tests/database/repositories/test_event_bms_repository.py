from datetime import datetime
from unittest.mock import MagicMock

from pyloninsight.database.repositories.event_bms import (
    EventBMSRepository,
)
from pyloninsight.models.event import Event


def make_bms_event(item: int = 1) -> Event:
    """Create a representative BMS event for testing."""

    return Event(
        item=item,
        timestamp=datetime(2026, 7, 13, 20, 19, 30),
        event_code="BHV",
        values={
            "stack_voltage": 52000,
            "stack_current": 1200,
            "temperature": 25,
            "battery_temp_low": 24,
            "battery_temp_high": 27,
            "battery_voltage_low": 3450,
            "battery_voltage_high": 3500,
            "unit_temp_low": 23,
            "unit_temp_high": 28,
            "unit_voltage_low": 3440,
            "unit_voltage_high": 3510,
            "base_state": "Normal",
            "voltage_state": "Normal",
            "current_state": "Normal",
            "temperature_state": "Normal",
            "state_of_charge": 97,
            "error_code": "0x00",
            "events": "BHV",
            "battery_events": "",
            "unit_events": "",
        },
    )


def test_create_many_bms_events():
    cursor = MagicMock()
    cursor.fetchall.return_value = [(101,), (102,)]

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMSRepository(connection)

    events = [
        make_bms_event(item=1),
        make_bms_event(item=2),
    ]

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=events,
    )

    assert event_ids == [101, 102]

    cursor.execute.assert_called_once()

    args, kwargs = cursor.execute.call_args

    assert "INSERT INTO event_bms" in args[0]
    assert "RETURNING id" in args[0]

    parameters = args[1]

    # Each event contributes 23 values.
    assert len(parameters) == 46

    # First event.
    assert parameters[0:4] == [
        12,
        1,
        datetime(2026, 7, 13, 20, 19, 30),
        52000,
    ]

    assert parameters[18:23] == [
        97,
        "0x00",
        "BHV",
        "",
        "",
    ]

    # Second event.
    assert parameters[23:26] == [
        12,
        2,
        datetime(2026, 7, 13, 20, 19, 30),
    ]

    assert kwargs == {}


def test_create_many_bms_events_with_empty_list():
    connection = MagicMock()

    repository = EventBMSRepository(connection)

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=[],
    )

    assert event_ids == []
    connection.cursor.assert_not_called()


def test_get_bms_event_by_id():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        1,
        datetime(2026, 7, 13, 20, 19, 30),
        52000,
        1200,
        25,
        24,
        27,
        3450,
        3500,
        23,
        28,
        3440,
        3510,
        "Normal",
        "Normal",
        "Normal",
        "Normal",
        97,
        "0x00",
        "BHV",
        "",
        "",
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMSRepository(connection)

    event = repository.get_by_id(101)

    assert event is not None
    assert event.item == 1
    assert event.timestamp == datetime(2026, 7, 13, 20, 19, 30)
    assert event.event_code == "BHV"

    assert event.values == {
        "stack_voltage": 52000,
        "stack_current": 1200,
        "temperature": 25,
        "battery_temp_low": 24,
        "battery_temp_high": 27,
        "battery_voltage_low": 3450,
        "battery_voltage_high": 3500,
        "unit_temp_low": 23,
        "unit_temp_high": 28,
        "unit_voltage_low": 3440,
        "unit_voltage_high": 3510,
        "base_state": "Normal",
        "voltage_state": "Normal",
        "current_state": "Normal",
        "temperature_state": "Normal",
        "state_of_charge": 97,
        "error_code": "0x00",
        "events": "BHV",
        "battery_events": "",
        "unit_events": "",
    }

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[1] == {}


def test_get_bms_event_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMSRepository(connection)

    event = repository.get_by_id(999)

    assert event is None
    cursor.execute.assert_called_once_with(
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
        (999,),
    )
