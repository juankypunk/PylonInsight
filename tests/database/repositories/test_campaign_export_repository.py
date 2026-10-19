from datetime import datetime
from unittest.mock import MagicMock

from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.models.campaign_export import CampaignExport


def test_create_campaign_export():
    cursor = MagicMock()
    cursor.fetchone.return_value = (12,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    export_timestamp = datetime(2026, 7, 9, 10, 30)

    campaign_export = CampaignExport(
        role="BMU1",
        export_timestamp=export_timestamp,
    )

    repository = CampaignExportRepository(connection)

    export_id = repository.create(
        campaign_id=3,
        device_id=7,
        campaign_export=campaign_export,
    )

    assert export_id == 12

    cursor.execute.assert_called_once_with(
        """
                INSERT INTO campaign_export (
                    campaign_id,
                    device_id,
                    role,
                    export_timestamp,
                    history_present,
                    events_present,
                    scanlog_present
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
        (
            3,
            7,
            "BMU1",
            export_timestamp,
            False,
            False,
            False,
        ),
    )

    connection.commit.assert_called_once_with()


def test_get_campaign_export_by_id():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        12,
        3,
        7,
        "BMU1",
        datetime(2026, 7, 9, 10, 30),
        True,
        True,
        False,
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = CampaignExportRepository(connection)

    campaign_export = repository.get_by_id(12)

    assert campaign_export is not None
    assert campaign_export.role == "BMU1"
    assert campaign_export.export_timestamp == datetime(2026, 7, 9, 10, 30)

    assert campaign_export.device is None
    assert campaign_export.snapshot is None
    assert campaign_export.files is not None
    assert campaign_export.history == []
    assert campaign_export.events == []

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    campaign_id,
                    device_id,
                    role,
                    export_timestamp,
                    history_present,
                    events_present,
                    scanlog_present
                FROM campaign_export
                WHERE id = %s
                """,
        (12,),
    )


def test_get_campaign_export_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = CampaignExportRepository(connection)

    campaign_export = repository.get_by_id(999)

    assert campaign_export is None

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    campaign_id,
                    device_id,
                    role,
                    export_timestamp,
                    history_present,
                    events_present,
                    scanlog_present
                FROM campaign_export
                WHERE id = %s
                """,
        (999,),
    )
