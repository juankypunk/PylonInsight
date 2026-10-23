from datetime import datetime
from unittest.mock import MagicMock

from pyloninsight.database.repositories.event_bmu import (
    EventBMURepository,
)
from pyloninsight.models.event import Event


def make_bmu_event(item: int = 1) -> Event:
    """Create a representative BMU event for testing."""

    return Event(
        item=item,
        timestamp=datetime(2026, 7, 13, 20, 19, 30),
        event_code="BHV",
        values={
            "module_voltage": 52000,
            "module_temperature": 25,
            "temperature_low": 24,
            "temperature_high": 27,
            "cell_voltage_low": 3450,
            "cell_voltage_high": 3500,
            "voltage_state": "Normal",
            "temperature_state": "Normal",
            "events": "Normal",
            "battery_events": "BHV",
        },
    )


def test_create_many_bmu_events():
    cursor = MagicMock()
    cursor.fetchall.return_value = [(101,), (102,)]

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMURepository(connection)

    events = [
        make_bmu_event(item=1),
        make_bmu_event(item=2),
    ]

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=events,
    )

    assert event_ids == [101, 102]

    cursor.execute.assert_called_once()

    args, kwargs = cursor.execute.call_args

    assert "INSERT INTO event_bmu" in args[0]
    assert "RETURNING id" in args[0]

    parameters = args[1]

    # Each event contributes 13 values.
    assert len(parameters) == 26

    # First event.
    assert parameters[0:5] == [
        12,
        1,
        datetime(2026, 7, 13, 20, 19, 30),
        52000,
        25,
    ]

    assert parameters[10:13] == [
        "Normal",
        "Normal",
        "BHV",
    ]

    # Second event.
    assert parameters[13:16] == [
        12,
        2,
        datetime(2026, 7, 13, 20, 19, 30),
    ]

    assert kwargs == {}


def test_create_many_bmu_events_with_empty_list():
    connection = MagicMock()

    repository = EventBMURepository(connection)

    event_ids = repository.create_many(
        campaign_export_id=12,
        events=[],
    )

    assert event_ids == []
    connection.cursor.assert_not_called()


def test_get_bmu_event_by_id():
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
        "Normal",
        "Normal",
        "Normal",
        "BHV",
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMURepository(connection)

    event = repository.get_by_id(101)

    assert event is not None
    assert event.item == 1
    assert event.timestamp == datetime(2026, 7, 13, 20, 19, 30)
    assert event.event_code == "BHV"

    assert event.values == {
        "module_voltage": 52000,
        "module_temperature": 25,
        "temperature_low": 24,
        "temperature_high": 27,
        "cell_voltage_low": 3450,
        "cell_voltage_high": 3500,
        "voltage_state": "Normal",
        "temperature_state": "Normal",
        "events": "Normal",
        "battery_events": "BHV",
    }

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[1] == {}


def test_get_bmu_event_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = EventBMURepository(connection)

    event = repository.get_by_id(999)

    assert event is None

    cursor.execute.assert_called_once_with(
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
        (999,),
    )
