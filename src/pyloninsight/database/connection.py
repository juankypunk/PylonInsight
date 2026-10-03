from __future__ import annotations

import os
from dataclasses import dataclass

import psycopg


class DatabaseConfigurationError(ValueError):
    """Raised when the PostgreSQL configuration is incomplete or invalid."""


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """PostgreSQL connection configuration."""

    host: str | None = None
    port: int = 5432
    database: str = ""
    user: str = ""
    password: str | None = None

    @classmethod
    def from_environment(cls) -> DatabaseConfig:
        """Build the configuration from PylonInsight environment variables."""

        host = os.getenv("PYLONINSIGHT_DB_HOST")
        database = os.getenv("PYLONINSIGHT_DB_NAME")
        user = os.getenv("PYLONINSIGHT_DB_USER")
        password = os.getenv("PYLONINSIGHT_DB_PASSWORD")

        missing = [
            name
            for name, value in (
                ("PYLONINSIGHT_DB_NAME", database),
                ("PYLONINSIGHT_DB_USER", user),
            )
            if not value
        ]

        if missing:
            raise DatabaseConfigurationError(
                "Missing PostgreSQL configuration: " + ", ".join(missing)
            )

        port_value = os.getenv("PYLONINSIGHT_DB_PORT", "5432")

        try:
            port = int(port_value)
        except ValueError as exc:
            raise DatabaseConfigurationError(
                "PYLONINSIGHT_DB_PORT must be an integer"
            ) from exc

        if not 1 <= port <= 65535:
            raise DatabaseConfigurationError(
                "PYLONINSIGHT_DB_PORT must be between 1 and 65535"
            )

        return cls(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )


def connect(config: DatabaseConfig) -> psycopg.Connection:
    """Open a PostgreSQL connection using the supplied configuration."""

    kwargs = {
        "port": config.port,
        "dbname": config.database,
        "user": config.user,
    }

    if config.host is not None:
        kwargs["host"] = config.host

    if config.password is not None:
        kwargs["password"] = config.password

    return psycopg.connect(**kwargs)
