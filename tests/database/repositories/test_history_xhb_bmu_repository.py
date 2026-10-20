"""Tests for the XHB_BMU_NT history repository."""

import logging
from datetime import datetime
from unittest.mock import MagicMock

from pyloninsight.database.repositories.history_xhb_bmu import (
    HistoryXHBBMURepository,
)
from pyloninsight.models.history import History


def make_history(
    timestamp: datetime | None = None,
    **overrides,
) -> History:
    """Create a representative XHB_BMU_NT history record."""
    values = {
        "module_voltage": 52000,
        "module_temperature": 25,
        "battery_temp_low": 24,
        "battery_temp_high": 27,
        "battery_voltage_low": 3400,
        "battery_voltage_high": 3500,
        "positive_terminal_temperature": 26,
        "negative_terminal_temperature": 25,
        "reference_voltage": 2500,
        "fan_pwm": 30,
        "fan1_rpm": 1200,
        "fan2_rpm": 1180,
        "base_state": "Normal",
        "voltage_state": "Normal",
        "temperature_state": "Normal",
        "positive_terminal_temperature_state": "Normal",
        "negative_terminal_temperature_state": "Normal",
        "error_code": "",
        "events": "",
    }

    values.update(
        {key: value for key, value in overrides.items() if key != "timestamp"}
    )

    if "timestamp" not in overrides and timestamp is None:
        timestamp = datetime(2026, 7, 1, 12, 0, 0)

    return History(
        timestamp=timestamp,
        values=values,
    )


def make_repository():
    """Create a repository with a mocked database connection."""
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    repository = HistoryXHBBMURepository(connection)

    return repository, connection, cursor


def get_record_values(record: History) -> tuple:
    """Return record values in database column order."""
    return tuple(record.values[key] for key in HistoryXHBBMURepository.VALUE_KEYS)


def make_existing_row(history_id: int, record: History) -> tuple:
    """Create a database row representing an existing measurement."""
    return (history_id, *get_record_values(record))


def test_create_many_inserts_new_measurement_and_association():
    """A new measurement is inserted and linked to its export."""
    repository, connection, cursor = make_repository()

    record = make_history()
    device_id = 10
    campaign_export_id = 20
    history_id = 100

    cursor.fetchone.return_value = (history_id,)

    result = repository.create_many(
        device_id=device_id,
        campaign_export_id=campaign_export_id,
        records=[record],
    )

    assert result == [history_id]
    assert cursor.execute.call_count == 2

    insert_call = cursor.execute.call_args_list[0]
    insert_sql = insert_call.args[0]
    insert_params = insert_call.args[1]

    assert "INSERT INTO history_xhb_bmu" in insert_sql
    assert "ON CONFLICT (device_id, record_timestamp) DO NOTHING" in insert_sql
    assert "RETURNING id" in insert_sql

    assert insert_params == (
        device_id,
        record.timestamp,
        *get_record_values(record),
    )

    association_call = cursor.execute.call_args_list[1]
    association_sql = association_call.args[0]
    association_params = association_call.args[1]

    assert "INSERT INTO history_xhb_bmu_export" in association_sql
    assert "ON CONFLICT" in association_sql
    assert association_params == (history_id, campaign_export_id)

    connection.commit.assert_called_once()


def test_create_many_reuses_existing_identical_measurement():
    """An identical measurement is reused instead of duplicated."""
    repository, connection, cursor = make_repository()

    record = make_history()
    device_id = 10
    campaign_export_id = 30
    history_id = 100

    cursor.fetchone.side_effect = [
        None,
        make_existing_row(history_id, record),
    ]

    result = repository.create_many(
        device_id=device_id,
        campaign_export_id=campaign_export_id,
        records=[record],
    )

    assert result == [history_id]
    assert cursor.execute.call_count == 3

    select_call = cursor.execute.call_args_list[1]
    select_sql = select_call.args[0]
    select_params = select_call.args[1]

    assert "SELECT id" in select_sql
    assert "FROM history_xhb_bmu" in select_sql
    assert "WHERE device_id = %s" in select_sql
    assert "record_timestamp = %s" in select_sql
    assert select_params == (device_id, record.timestamp)

    association_call = cursor.execute.call_args_list[2]
    assert association_call.args[1] == (
        history_id,
        campaign_export_id,
    )

    connection.commit.assert_called_once()


def test_create_many_keeps_existing_values_on_conflict(caplog):
    """Conflicting values do not overwrite an existing measurement."""
    repository, connection, cursor = make_repository()

    device_id = 10
    campaign_export_id = 30
    history_id = 100

    existing_record = make_history()
    conflicting_record = make_history(module_voltage=53000)

    cursor.fetchone.side_effect = [
        None,
        make_existing_row(history_id, existing_record),
    ]

    with caplog.at_level(logging.WARNING):
        result = repository.create_many(
            device_id=device_id,
            campaign_export_id=campaign_export_id,
            records=[conflicting_record],
        )

    assert result == [history_id]
    assert "Conflicting XHB_BMU_NT history values" in caplog.text
    assert "Keeping the existing measurement" in caplog.text

    executed_sql = [call.args[0] for call in cursor.execute.call_args_list]

    assert len(executed_sql) == 3
    assert all("UPDATE history_xhb_bmu" not in sql for sql in executed_sql)

    association_call = cursor.execute.call_args_list[2]
    assert association_call.args[1] == (
        history_id,
        campaign_export_id,
    )

    connection.commit.assert_called_once()


def test_create_many_skips_records_without_timestamp(caplog):
    """Records without timestamps are skipped."""
    repository, connection, cursor = make_repository()

    record = make_history()
    record.timestamp = None

    with caplog.at_level(logging.WARNING):
        result = repository.create_many(
            device_id=10,
            campaign_export_id=20,
            records=[record],
        )

    assert result == []
    assert "Skipping XHB_BMU_NT history record without a timestamp" in caplog.text

    connection.cursor.assert_not_called()
    cursor.execute.assert_not_called()
    connection.commit.assert_not_called()


def test_create_many_with_empty_list_does_nothing():
    """An empty input list does not access the database."""
    repository, connection, cursor = make_repository()

    result = repository.create_many(
        device_id=10,
        campaign_export_id=20,
        records=[],
    )

    assert result == []

    connection.cursor.assert_not_called()
    cursor.execute.assert_not_called()
    connection.commit.assert_not_called()
