from pathlib import Path

from pyloninsight.inspection.csv_structure import inspect_csv_structure


def test_inspect_real_xhb_bmu_event_csv():
    path = Path(
        "tests/data/minimal/campaign/batt1/events/" "UnknownSN_event_20260708120234.csv"
    )

    structure = inspect_csv_structure(path)

    assert structure.column_names[0] == "Item"
    assert structure.column_names[1] == "Time"
    assert structure.column_count == 21
    assert structure.data_row_count == 4
    assert structure.data_field_count == 23
    assert structure.data_field_counts == [23, 23, 23, 23]
    assert structure.has_inconsistent_data_fields is False


def test_inspect_csv_with_inconsistent_data_fields(tmp_path):
    path = tmp_path / "irregular.csv"

    path.write_text(
        """\
Item,Time,Value
0,12:00,100
1,12:01,101
2,12:02
3,12:03,103
Command,completed,successfully
$$
""",
        encoding="utf-8",
    )

    structure = inspect_csv_structure(path)

    assert structure.column_names == ["Item", "Time", "Value"]
    assert structure.column_count == 3
    assert structure.data_row_count == 4
    assert structure.data_field_count == 3
    assert structure.data_field_counts == [3, 3, 2, 3]
    assert structure.has_inconsistent_data_fields is True
