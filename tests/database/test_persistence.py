from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from pyloninsight.database.persistence import CampaignPersistence
from pyloninsight.models.campaign import Campaign
from pyloninsight.models.campaign_export import CampaignExport
from pyloninsight.models.device import Device

from pyloninsight.models.device_snapshot import DeviceSnapshot
from pyloninsight.models.event import Event
from pyloninsight.models.history import History


@pytest.fixture
def persistence():
    with (
        patch("pyloninsight.database.persistence.CampaignRepository") as campaign_repo,
        patch("pyloninsight.database.persistence.DeviceRepository") as device_repo,
        patch(
            "pyloninsight.database.persistence.CampaignExportRepository"
        ) as export_repo,
        patch(
            "pyloninsight.database.persistence.DeviceSnapshotRepository"
        ) as snapshot_repo,
        patch("pyloninsight.database.persistence.HistoryBMSRepository") as history_repo,
        patch(
            "pyloninsight.database.persistence.EVENT_REPOSITORIES",
            new_callable=dict,
        ) as event_repositories,
    ):
        # Sustituir el diccionario por fábricas que devuelven mocks
        event_bms = MagicMock()
        event_bmu = MagicMock()
        event_xhb_bmu = MagicMock()

        event_repositories.update(
            {
                "CMU_A": lambda connection: event_bms,
                "bmu": lambda connection: event_bmu,
                "XHB_BMU_NT": lambda connection: event_xhb_bmu,
            }
        )

        connection = MagicMock()
        instance = CampaignPersistence(connection)

        # Guardamos referencias para que las pruebas puedan verificarlas.
        instance._test_event_bms = event_bms
        instance._test_event_bmu = event_bmu
        instance._test_event_xhb_bmu = event_xhb_bmu

        yield instance

        campaign_repo.assert_called_once_with(connection)
        device_repo.assert_called_once_with(connection)
        export_repo.assert_called_once_with(connection)
        snapshot_repo.assert_called_once_with(connection)
        history_repo.assert_called_once_with(connection)


@pytest.fixture
def campaign():
    device = Device(
        barcode="TEST-BMS-001",
        device_type="BMS",
        manufacturer="Pylontech",
        model="CMU_A",
    )

    export = CampaignExport(
        role="BMS",
        export_timestamp=datetime(2026, 7, 1, 12, 0, 0),
        device=device,
    )

    return Campaign(
        name="test-campaign",
        capture_date=datetime(2026, 7, 1),
        exports=[export],
    )


def test_save_creates_campaign(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    campaign_id = persistence.save(campaign)

    assert campaign_id == 42
    persistence.campaign_repository.create.assert_called_once_with(campaign)


def test_save_reuses_existing_device(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    persistence.save(campaign)

    persistence.device_repository.get_id_by_barcode.assert_called_once_with(
        "TEST-BMS-001"
    )
    persistence.device_repository.create.assert_not_called()


def test_save_creates_device_when_barcode_is_unknown(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = None
    persistence.device_repository.create.return_value = 7
    persistence.export_repository.create.return_value = 101

    persistence.save(campaign)

    persistence.device_repository.create.assert_called_once_with(
        campaign.exports[0].device
    )


def test_save_skips_export_without_device(persistence):
    campaign = Campaign(
        name="campaign-without-device",
        capture_date=datetime(2026, 7, 1),
        exports=[CampaignExport(role="BMS")],
    )
    persistence.campaign_repository.create.return_value = 42

    campaign_id = persistence.save(campaign)

    assert campaign_id == 42
    persistence.export_repository.create.assert_not_called()


def test_save_skips_export_without_barcode(persistence):
    device = Device(
        barcode="",
        device_type="BMS",
        manufacturer="Pylontech",
        model="CMU_A",
    )
    campaign = Campaign(
        name="campaign-without-barcode",
        capture_date=datetime(2026, 7, 1),
        exports=[CampaignExport(role="BMS", device=device)],
    )
    persistence.campaign_repository.create.return_value = 42

    campaign_id = persistence.save(campaign)

    assert campaign_id == 42
    persistence.device_repository.create.assert_not_called()
    persistence.export_repository.create.assert_not_called()


def test_save_persists_snapshot(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    snapshot = DeviceSnapshot(
        snapshot_timestamp=datetime(2026, 7, 1, 12, 0, 0),
        board_version="TISP01V10R02_1",
        hardware_version="V10R9C5",
    )
    campaign.exports[0].snapshot = snapshot

    persistence.save(campaign)

    persistence.snapshot_repository.create.assert_called_once_with(
        campaign_export_id=101,
        snapshot=snapshot,
    )


def test_save_skips_missing_snapshot(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    campaign.exports[0].snapshot = None

    persistence.save(campaign)

    persistence.snapshot_repository.create.assert_not_called()


def test_save_persists_bms_history(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    records = [
        History(
            timestamp=datetime(2026, 7, 1, 12, 0, 0),
            values={"soc": 75},
        )
    ]
    campaign.exports[0].history = records

    persistence.save(campaign)

    persistence.history_bms_repository.create_many.assert_called_once_with(
        device_id=7,
        campaign_export_id=101,
        records=records,
    )


def test_save_persists_bms_events(persistence, campaign):
    persistence.campaign_repository.create.return_value = 42
    persistence.device_repository.get_id_by_barcode.return_value = 7
    persistence.export_repository.create.return_value = 101

    events = [
        Event(
            item=1,
            timestamp=datetime(2026, 7, 1, 12, 0, 0),
            event_code="BHV",
            description="Example event",
            values={"soc": 75},
        )
    ]
    campaign.exports[0].events = events

    persistence.save(campaign)

    event_repository = persistence.event_repositories["CMU_A"]
    event_repository.create_many.assert_called_once_with(
        campaign_export_id=101,
        events=events,
    )
