from __future__ import annotations

import psycopg

from pyloninsight.models.campaign import Campaign


class CampaignRepository:
    """Persistence operations for Campaign objects."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create(self, campaign: Campaign) -> int:
        """Create a campaign and return its database ID."""

        if campaign.created_at is None:
            query = """
                INSERT INTO campaign (
                    name,
                    capture_date,
                    description
                )
                VALUES (%s, %s, %s)
                RETURNING id
            """
            params = (
                campaign.name,
                campaign.capture_date,
                campaign.description,
            )
        else:
            query = """
                INSERT INTO campaign (
                    name,
                    capture_date,
                    description,
                    created_at
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            params = (
                campaign.name,
                campaign.capture_date,
                campaign.description,
                campaign.created_at,
            )

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            campaign_id = cursor.fetchone()[0]

        self.connection.commit()

        return campaign_id

    def get_by_id(self, campaign_id: int) -> Campaign | None:
        """Return a campaign by database ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
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
                (campaign_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        _, name, capture_date, description, created_at = row

        return Campaign(
            name=name,
            capture_date=capture_date,
            created_at=created_at,
            description=description,
        )
