from unittest.mock import MagicMock
from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.models.campaign import Campaign
from datetime import datetime


def test_create_campaign_uses_database_default_for_created_at():
    cursor = MagicMock()
    cursor.fetchone.return_value = (42,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    campaign = Campaign(
        name="2026-07-13_SOC100",
        capture_date=None,
        created_at=None,
        description="Test campaign",
    )

    repository = CampaignRepository(connection)

    campaign_id = repository.create(campaign)

    assert campaign_id == 42

    cursor.execute.assert_called_once_with(
        """
                INSERT INTO campaign (
                    name,
                    capture_date,
                    description
                )
                VALUES (%s, %s, %s)
                RETURNING id
            """,
        (
            "2026-07-13_SOC100",
            None,
            "Test campaign",
        ),
    )

    connection.commit.assert_called_once_with()


def test_create_campaign_uses_explicit_created_at():
    cursor = MagicMock()
    cursor.fetchone.return_value = (43,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    created_at = datetime(2026, 10, 2, 9, 30, 0)

    campaign = Campaign(
        name="test-campaign",
        capture_date=datetime(2026, 7, 13, 20, 19, 30),
        created_at=created_at,
        description="Test campaign",
    )

    repository = CampaignRepository(connection)

    campaign_id = repository.create(campaign)

    assert campaign_id == 43

    cursor.execute.assert_called_once_with(
        """
                INSERT INTO campaign (
                    name,
                    capture_date,
                    description,
                    created_at
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """,
        (
            "test-campaign",
            datetime(2026, 7, 13, 20, 19, 30),
            "Test campaign",
            created_at,
        ),
    )

    connection.commit.assert_called_once_with()


def test_get_campaign_by_id():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        42,
        "2026-07-13_SOC100",
        datetime(2026, 7, 13, 20, 19, 30),
        "Test campaign",
        datetime(2026, 10, 2, 9, 30, 0),
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = CampaignRepository(connection)

    campaign = repository.get_by_id(42)

    assert campaign is not None
    assert campaign.name == "2026-07-13_SOC100"
    assert campaign.capture_date == datetime(2026, 7, 13, 20, 19, 30)
    assert campaign.description == "Test campaign"
    assert campaign.created_at == datetime(2026, 10, 2, 9, 30, 0)

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    name,
                    capture_date,
                    description,
                    created_at
                FROM campaign
                WHERE id = %s
                """,
        (42,),
    )


def test_get_campaign_by_id_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = CampaignRepository(connection)

    campaign = repository.get_by_id(999)

    assert campaign is None

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    id,
                    name,
                    capture_date,
                    description,
                    created_at
                FROM campaign
                WHERE id = %s
                """,
        (999,),
    )
