from pathlib import Path

from pyloninsight.inspection.csv_structure import inspect_csv_structure


def test_inspect_csv_structure(tmp_path: Path) -> None:
    path = tmp_path / "test.csv"

    path.write_text(
        """\
Name,Value,Status
A,10,OK
B,20,OK
""",
        encoding="utf-8",
    )

    structure = inspect_csv_structure(path)

    assert structure.path == path
    assert structure.column_names == ["Name", "Value", "Status"]
    assert structure.column_count == 3
    assert structure.data_row_count == 2
