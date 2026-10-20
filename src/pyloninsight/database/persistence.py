"""Coordinate persistence of complete BatteryView campaigns."""

from __future__ import annotations

import logging

import psycopg

from pyloninsight.database.repositories.campaign import CampaignRepository
from pyloninsight.database.repositories.campaign_export import (
    CampaignExportRepository,
)
from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.database.repositories.device_snapshot import (
    DeviceSnapshotRepository,
)
from pyloninsight.database.repositories.event_bms import EventBMSRepository
from pyloninsight.database.repositories.event_bmu import EventBMURepository
from pyloninsight.database.repositories.event_xhb_bmu import (
    EventXHBMURepository,
)
from pyloninsight.database.repositories.history_bms import (
    HistoryBMSRepository,
)
from pyloninsight.database.repositories.history_bmu import (
    HistoryBMURepository,
)
from pyloninsight.database.repositories.history_xhb_bmu import (
    HistoryXHBBMURepository,
)
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.device import Device

logger = logging.getLogger(__name__)


EVENT_REPOSITORIES = {
    "CMU_A": EventBMSRepository,
    "bmu": EventBMURepository,
    "XHB_BMU_NT": EventXHBMURepository,
}


class CampaignPersistence:
    """Persist campaigns and their associated exports and measurements."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

        self.campaign_repository = CampaignRepository(connection)
        self.device_repository = DeviceRepository(connection)
        self.export_repository = CampaignExportRepository(connection)
        self.snapshot_repository = DeviceSnapshotRepository(connection)
        self.history_bms_repository = HistoryBMSRepository(connection)
        self.history_bmu_repository = HistoryBMURepository(connection)
        self.history_xhb_bmu_repository = HistoryXHBBMURepository(connection)

        self.event_repositories = {
            model: repository(connection)
            for model, repository in EVENT_REPOSITORIES.items()
        }

    def save(self, campaign: Campaign) -> int:
        """Persist a campaign and return its database ID."""
        campaign_id = self.campaign_repository.create(campaign)

        for export in campaign.exports:
            device = export.device

            if device is None:
                logger.warning(
                    "Skipping export %s in campaign %s: no device metadata",
                    export.role,
                    campaign.name,
                )
                continue

            if not device.barcode:
                logger.warning(
                    "Skipping export %s in campaign %s: " "device has no barcode",
                    export.role,
                    campaign.name,
                )
                continue

            device_id = self.device_repository.get_id_by_barcode(device.barcode)

            if device_id is None:
                device_id = self.device_repository.create(device)

            export_id = self.export_repository.create(
                campaign_id=campaign_id,
                device_id=device_id,
                campaign_export=export,
            )

            if export.snapshot is not None:
                self.snapshot_repository.create(
                    campaign_export_id=export_id,
                    snapshot=export.snapshot,
                )

            if export.history:
                if device.model == "CMU_A":
                    self.history_bms_repository.create_many(
                        device_id=device_id,
                        campaign_export_id=export_id,
                        records=export.history,
                    )
                elif device.model == "bmu":
                    self.history_bmu_repository.create_many(
                        device_id=device_id,
                        campaign_export_id=export_id,
                        records=export.history,
                    )
                elif device.model == "XHB_BMU_NT":
                    self.history_xhb_bmu_repository.create_many(
                        device_id=device_id,
                        campaign_export_id=export_id,
                        records=export.history,
                    )

            event_repository = self.event_repositories.get(device.model)

            if event_repository is not None and export.events:
                event_repository.create_many(
                    campaign_export_id=export_id,
                    events=export.events,
                )

        return campaign_id
