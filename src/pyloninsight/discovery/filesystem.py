from pathlib import Path

from pyloninsight.models.export_files import ExportFiles

from .errors import DuplicateExportFileError, MissingDeviceExportError


def discover_export_files(device_dir: Path) -> ExportFiles:
    """
    Discover all export files belonging to one BatteryView device.

    Required exports:
        - history CSV
        - events CSV

    Optional exports:
        - history TXT
        - history detailed TXT
        - events TXT
        - events detailed TXT
        - scanlog CSV
    """

    files = ExportFiles()

    #
    # History
    #
    history_dir = device_dir / "history"

    if not history_dir.is_dir():
        raise MissingDeviceExportError(f"Missing history directory: {history_dir}")

    for file in history_dir.iterdir():

        if file.suffix == ".csv":

            if files.history_csv is not None:
                raise DuplicateExportFileError(
                    f"Multiple history CSV files found in: {history_dir}"
                )

            files.history_csv = file

        elif file.name.endswith("_detailed.txt"):

            if files.history_detailed is not None:
                raise DuplicateExportFileError(
                    f"Multiple history detailed TXT files found in: {history_dir}"
                )

            files.history_detailed = file

        elif file.suffix == ".txt":

            if files.history_txt is not None:
                raise DuplicateExportFileError(
                    f"Multiple history TXT files found in: {history_dir}"
                )

            files.history_txt = file

    if files.history_csv is None:
        raise MissingDeviceExportError(f"Missing history CSV file in: {history_dir}")

    #
    # Events
    #
    events_dir = device_dir / "events"

    if not events_dir.is_dir():
        raise MissingDeviceExportError(f"Missing events directory: {events_dir}")

    for file in events_dir.iterdir():

        if file.suffix == ".csv":

            if files.event_csv is not None:
                raise DuplicateExportFileError(
                    f"Multiple event CSV files found in: {events_dir}"
                )

            files.event_csv = file

        elif file.name.endswith("_detailed.txt"):

            if files.event_detailed is not None:
                raise DuplicateExportFileError(
                    f"Multiple event detailed TXT files found in: {events_dir}"
                )

            files.event_detailed = file

        elif file.suffix == ".txt":

            if files.event_txt is not None:
                raise DuplicateExportFileError(
                    f"Multiple event TXT files found in: {events_dir}"
                )

            files.event_txt = file

    if files.event_csv is None:
        raise MissingDeviceExportError(f"Missing event CSV file in: {events_dir}")

    #
    # Scanlog (optional)
    #
    scanlog_dir = device_dir / "scanlog"

    if scanlog_dir.is_dir():

        scanlog = scanlog_dir / "scanlog.csv"

        if scanlog.exists():
            files.scanlog_csv = scanlog

    return files
