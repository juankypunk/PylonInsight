from unittest.mock import MagicMock

from pyloninsight.database.repositories.device import DeviceRepository
from pyloninsight.models.device import Device


def test_create_device():
    cursor = MagicMock()
    cursor.fetchone.return_value = (7,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    device = Device(
        barcode="TEST-BARCODE-001",
        device_type="BMU",
        manufacturer="Pylontech",
        model="bmu",
        specification="48V/50Ah",
        notes="Test device",
    )

    repository = DeviceRepository(connection)

    device_id = repository.create(device)

    assert device_id == 7

    cursor.execute.assert_called_once_with(
        """
                INSERT INTO device (
                    barcode,
                    device_type,
                    manufacturer,
                    model,
                    specification,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
        (
            "TEST-BARCODE-001",
            "BMU",
            "Pylontech",
            "bmu",
            "48V/50Ah",
            "Test device",
        ),
    )



def test_get_device_by_barcode():
    cursor = MagicMock()
    cursor.fetchone.return_value = (
        "TEST-BARCODE-001",
        "BMU",
        "Pylontech",
        "bmu",
        "48V/50Ah",
        "Test device",
    )

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceRepository(connection)

    device = repository.get_by_barcode("TEST-BARCODE-001")

    assert device is not None
    assert device.barcode == "TEST-BARCODE-001"
    assert device.device_type == "BMU"
    assert device.manufacturer == "Pylontech"
    assert device.model == "bmu"
    assert device.specification == "48V/50Ah"
    assert device.notes == "Test device"

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    barcode,
                    device_type,
                    manufacturer,
                    model,
                    specification,
                    notes
                FROM device
                WHERE barcode = %s
                """,
        ("TEST-BARCODE-001",),
    )


def test_get_device_by_barcode_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceRepository(connection)

    device = repository.get_by_barcode("UNKNOWN-BARCODE")

    assert device is None

    cursor.execute.assert_called_once_with(
        """
                SELECT
                    barcode,
                    device_type,
                    manufacturer,
                    model,
                    specification,
                    notes
                FROM device
                WHERE barcode = %s
                """,
        ("UNKNOWN-BARCODE",),
    )


def test_get_device_id_by_barcode():
    cursor = MagicMock()
    cursor.fetchone.return_value = (7,)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceRepository(connection)

    device_id = repository.get_id_by_barcode("TEST-BARCODE-001")

    assert device_id == 7

    cursor.execute.assert_called_once_with(
        """
                SELECT id
                FROM device
                WHERE barcode = %s
                """,
        ("TEST-BARCODE-001",),
    )


def test_get_device_id_by_barcode_returns_none_when_not_found():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    repository = DeviceRepository(connection)

    device_id = repository.get_id_by_barcode("UNKNOWN-BARCODE")

    assert device_id is None

    cursor.execute.assert_called_once_with(
        """
                SELECT id
                FROM device
                WHERE barcode = %s
                """,
        ("UNKNOWN-BARCODE",),
    )
