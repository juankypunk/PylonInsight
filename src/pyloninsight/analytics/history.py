from dataclasses import dataclass
from datetime import datetime

from pyloninsight.models.history import History


@dataclass
class HistoryAnomaly:
    type: str
    record_index: int
    timestamp: datetime | None
    previous_timestamp: datetime | None = None


def analyze_history(records: list[History]) -> list[HistoryAnomaly]:
    """
    Analyze history records and detect timestamp anomalies.

    The function does not modify or discard records.

    Detected anomalies:

    - invalid_timestamp:
        The record has no valid timestamp.

    - timestamp_regression:
        The record timestamp is earlier than the timestamp
        of the previous record.
    """

    anomalies = []

    previous_timestamp = None

    for index, record in enumerate(records):

        timestamp = record.timestamp

        if timestamp is None:
            anomalies.append(
                HistoryAnomaly(
                    type="invalid_timestamp",
                    record_index=index,
                    timestamp=None,
                    previous_timestamp=previous_timestamp,
                )
            )

            continue

        if previous_timestamp is not None and timestamp < previous_timestamp:
            anomalies.append(
                HistoryAnomaly(
                    type="timestamp_regression",
                    record_index=index,
                    timestamp=timestamp,
                    previous_timestamp=previous_timestamp,
                )
            )

        previous_timestamp = timestamp

    return anomalies
