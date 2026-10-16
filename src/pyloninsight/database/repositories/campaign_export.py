from __future__ import annotations

import psycopg

from pyloninsight.models.campaign_export import CampaignExport


class CampaignExportRepository:
    """Persistence operations for CampaignExport objects."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create(
        self,
        campaign_id: int,
        device_id: int,
        campaign_export: CampaignExport,
    ) -> int:
        """Create a campaign export and return its database ID."""

        with self.connection.cursor() as cursor:
            cursor.execute(
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
                    campaign_id,
                    device_id,
                    campaign_export.role,
                    campaign_export.export_timestamp,
                    bool(campaign_export.history),
                    bool(campaign_export.events),
                    False,
                ),
            )

            export_id = cursor.fetchone()[0]

        self.connection.commit()

        return export_id

    def get_by_id(self, export_id: int) -> CampaignExport | None:
        """Return a campaign export by database ID, or None if it does not exist."""

        with self.connection.cursor() as cursor:
            cursor.execute(
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
                (export_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        (
            _,
            _campaign_id,
            _device_id,
            role,
            export_timestamp,
            _history_present,
            _events_present,
            _scanlog_present,
        ) = row

        return CampaignExport(
            role=role,
            export_timestamp=export_timestamp,
        )
