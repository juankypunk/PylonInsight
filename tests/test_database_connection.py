import pytest

from pyloninsight.database.connection import (
    DatabaseConfig,
    DatabaseConfigurationError,
)


def test_config_from_environment(monkeypatch):
    monkeypatch.setenv("PYLONINSIGHT_DB_HOST", "db.example")
    monkeypatch.setenv("PYLONINSIGHT_DB_PORT", "5433")
    monkeypatch.setenv("PYLONINSIGHT_DB_NAME", "pyloninsight")
    monkeypatch.setenv("PYLONINSIGHT_DB_USER", "pylon")
    monkeypatch.setenv("PYLONINSIGHT_DB_PASSWORD", "secret")

    config = DatabaseConfig.from_environment()

    assert config.host == "db.example"
    assert config.port == 5433
    assert config.database == "pyloninsight"
    assert config.user == "pylon"
    assert config.password == "secret"


def test_config_uses_default_port(monkeypatch):
    monkeypatch.setenv("PYLONINSIGHT_DB_HOST", "localhost")
    monkeypatch.setenv("PYLONINSIGHT_DB_NAME", "pyloninsight")
    monkeypatch.setenv("PYLONINSIGHT_DB_USER", "pylon")
    monkeypatch.setenv("PYLONINSIGHT_DB_PASSWORD", "secret")

    monkeypatch.delenv("PYLONINSIGHT_DB_PORT", raising=False)

    config = DatabaseConfig.from_environment()

    assert config.port == 5432


def test_config_requires_mandatory_variables(monkeypatch):
    for variable in (
        "PYLONINSIGHT_DB_NAME",
        "PYLONINSIGHT_DB_USER",
    ):
        monkeypatch.delenv(variable, raising=False)

    with pytest.raises(DatabaseConfigurationError) as exc_info:
        DatabaseConfig.from_environment()

    message = str(exc_info.value)

    assert "PYLONINSIGHT_DB_NAME" in message
    assert "PYLONINSIGHT_DB_USER" in message


def test_config_rejects_invalid_port(monkeypatch):
    monkeypatch.setenv("PYLONINSIGHT_DB_HOST", "localhost")
    monkeypatch.setenv("PYLONINSIGHT_DB_NAME", "pyloninsight")
    monkeypatch.setenv("PYLONINSIGHT_DB_USER", "pylon")
    monkeypatch.setenv("PYLONINSIGHT_DB_PASSWORD", "secret")
    monkeypatch.setenv("PYLONINSIGHT_DB_PORT", "not-a-port")

    with pytest.raises(DatabaseConfigurationError, match="must be an integer"):
        DatabaseConfig.from_environment()


def test_config_rejects_port_outside_valid_range(monkeypatch):
    monkeypatch.setenv("PYLONINSIGHT_DB_HOST", "localhost")
    monkeypatch.setenv("PYLONINSIGHT_DB_NAME", "pyloninsight")
    monkeypatch.setenv("PYLONINSIGHT_DB_USER", "pylon")
    monkeypatch.setenv("PYLONINSIGHT_DB_PASSWORD", "secret")
    monkeypatch.setenv("PYLONINSIGHT_DB_PORT", "70000")

    with pytest.raises(
        DatabaseConfigurationError,
        match="between 1 and 65535",
    ):
        DatabaseConfig.from_environment()


from unittest.mock import patch

from pyloninsight.database.connection import DatabaseConfig, connect


def test_connect_passes_config_to_psycopg():
    config = DatabaseConfig(
        port=5433,
        database="pyloninsight",
        user="juanky",
    )
    fake_connection = object()

    with patch(
        "pyloninsight.database.connection.psycopg.connect",
        return_value=fake_connection,
    ) as mock_connect:
        result = connect(config)

    assert result is fake_connection

    mock_connect.assert_called_once_with(
        port=5433,
        dbname="pyloninsight",
        user="juanky",
    )


def test_config_allows_local_peer_authentication(monkeypatch):
    monkeypatch.setenv("PYLONINSIGHT_DB_NAME", "pyloninsight")
    monkeypatch.setenv("PYLONINSIGHT_DB_USER", "juanky")

    monkeypatch.delenv("PYLONINSIGHT_DB_HOST", raising=False)
    monkeypatch.delenv("PYLONINSIGHT_DB_PASSWORD", raising=False)

    config = DatabaseConfig.from_environment()

    assert config.host is None
    assert config.password is None
