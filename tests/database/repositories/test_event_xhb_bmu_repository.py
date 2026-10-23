from datetime import datetime
from unittest.mock import MagicMock

from pyloninsight.database.repositories.event_xhb_bmu import (
    EventXHBMURepository,
)
from pyloninsight.models.event import Event


def make_xhb_bmu_event(item: int = 1) -> Event:
    """Create a representative XHB BMU event for testing."""

    return Event(
        item=item,
        timestamp=datetime(2026, 7, 13, 20, 19, 30),
        event_code="SYSERR",
        values={
            "module_voltage": 52000,
            "module_temperature": 25,
            "temperature_low": 24,
            "temperature_high": 27,
            "cell_voltage_low": 3450,
            "cell_voltage_high": 3500,
            "positive_terminal_temperature": 26,
            "negative_terminal_temperature": 27,
            "reference_voltage": 3000,
            "fan_pwm": 50,
            "fan1_rpm": 1200,
            "fan2_rpm": 1180,
            "base_state": "SysError",
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "positive_terminal_temperature_state": "Normal",
            "negative_terminal_temperature_state": "Normal",
            "error_code": "0x20",
            "events": "SYSERR",
        },
    )


def test_create_many_xhb_bmu_events():
    cursor = MagicMock()
    cursor.fetchall.return_value = [(101,), (102,)]

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventXHBMURepository(connection)

    events = [
        make_xhb_bmu_event(item=1),
        make_xhb_bmu_event(item=2),
    ]

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=events,
    )

    assert event_ids == [101, 102]

    cursor.execute.assert_called_once()

    args, kwargs = cursor.execute.call_args

    assert "INSERT INTO event_xhb_bmu" in args[0]
    assert "RETURNING id" in args[0]

    parameters = args[1]

    # Each event contributes 22 values.
    assert len(parameters) == 44

    # First event.
    assert parameters[0:5] == [
        12,
        1,
        datetime(2026, 7, 13, 20, 19, 30),
        52000,
        25,
    ]
    # Additional XHB BMU measurements.
    assert parameters[9:16] == [
        26,
        27,
        3000,
        50,
        1200,
        1180,
        "SysError",
    ]

    # Final status and error fields.
    assert parameters[20:22] == [
        "0x20",
        "SYSERR",
    ]

    # Second event.
    assert parameters[22:25] == [
        12,
        2,
        datetime(2026, 7, 13, 20, 19, 30),
    ]

    assert kwargs == {}


def test_create_many_xhb_bmu_events_with_empty_list():
    connection = MagicMock()

    repository = EventXHBMURepository(connection)

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=[],
    )

    assert event_ids == []
    connection.cursor.assert_not_called()


def test_get_xhb_bmu_event_by_id():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        1,
        datetime(2026, 7, 13, 20, 19, 30),
        52000,
        25,
        24,
        27,
        3450,
        3500,
        26,
        27,
        3000,
        50,
        1200,
        1180,
        "SysError",
        "Normal",
        "Normal",
        "Normal",
        "Normal",
        "0x20",
        "SYSERR",
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventXHBMURepository(connection)

    event = repository.get_by_id(101)

    assert event is not None
    assert event.item == 1
    assert event.timestamp == datetime(2026, 7, 13, 20, 19, 30)
    assert event.event_code == "SYSERR"

    assert event.values == {
        "module_voltage": 52000,
        "module_temperature": 25,
        "temperature_low": 24,
        "temperature_high": 27,
        "cell_voltage_low": 3450,
        "cell_voltage_high": 3500,
        "positive_terminal_temperature": 26,
        "negative_terminal_temperature": 27,
        "reference_voltage": 3000,
        "fan_pwm": 50,
        "fan1_rpm": 1200,
        "fan2_rpm": 1180,
        "base_state": "SysError",
        "voltage_state": "Normal",
        "temperature_state": "Normal",
        "positive_terminal_temperature_state": "Normal",
        "negative_terminal_temperature_state": "Normal",
        "error_code": "0x20",
        "events": "SYSERR",
    }

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[1] == {}


def test_get_xhb_bmu_event_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventXHBMURepository(connection)

    event = repository.get_by_id(999)

    assert event is None

    cursor.execute.assert_called_once_with(
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
        (999,),
    )
