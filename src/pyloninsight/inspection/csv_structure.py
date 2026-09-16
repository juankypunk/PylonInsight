from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class CsvStructure:
    path: Path
    column_names: list[str]
    column_count: int
    data_row_count: int
    data_field_count: int
    data_field_counts: list[int]

    @property
    def has_inconsistent_data_fields(self) -> bool:
        return len(set(self.data_field_counts)) > 1


def _looks_like_header(row: list[str]) -> bool:
    """
    Return True if a CSV row looks like a column-name header.
    """
    if not row:
        return False

    if row[0] in {"datalist", "@"}:
        return False

    return any(value and not value[0].isdigit() for value in row)


def inspect_csv_structure(path: Path) -> CsvStructure:
    """
    Inspect the basic structure of a CSV file.

    The CSV header is detected as the first non-empty row whose
    fields are not purely numeric/date-like data.
    """
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.reader(file)

        column_names = None
        data_rows: list[list[str]] = []

        for row in reader:
            if not row:
                continue

            if column_names is None:
                if _looks_like_header(row):
                    column_names = row
                continue

            if row[0].startswith("Command"):
                break

            if row[0] == "$$":
                break

            data_rows.append(row)

    if column_names is None:
        raise ValueError(f"Could not detect CSV column header: {path}")

    data_field_count = len(data_rows[0]) if data_rows else 0
    data_field_counts = [len(row) for row in data_rows]

    return CsvStructure(
        path=path,
        column_names=column_names,
        column_count=len(column_names),
        data_row_count=len(data_rows),
        data_field_count=data_field_count,
        data_field_counts=data_field_counts,
    )
