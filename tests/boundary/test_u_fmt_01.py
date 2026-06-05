"""U-FMT-01~03 (P1 / EXT-03): --format table | json | csv."""


def test_u_fmt_01_table_format_pipe_table(capsys):
    """U-FMT-01: format=table → | unit | input | result | 파이프 테이블 (그림 SSOT)."""
    from boundary.app import run_cli_with_format
    from tests._approval import assert_matches_golden

    run_cli_with_format("meter:2.5", output_format="table")
    captured = capsys.readouterr()

    assert_matches_golden(
        captured.out, "u_fmt_01_table_meter_25.approved.txt"
    )


def test_u_fmt_01_table_columns_present(capsys):
    """U-FMT-01: table 헤더 unit/input/result 및 3 data rows."""
    from boundary.app import run_cli_with_format

    run_cli_with_format("meter:2.5", output_format="table")
    captured = capsys.readouterr()
    out = captured.out.lower()

    assert "unit" in out and "input" in out and "result" in out, (
        f"RED: U-FMT-01 — table headers missing: {captured.out!r}"
    )
    assert out.count("|") >= 8, (
        f"RED: U-FMT-01 — pipe table expected, got {captured.out!r}"
    )
    data_lines = [
        ln
        for ln in captured.out.splitlines()
        if "|" in ln
        and "---" not in ln
        and "unit" not in ln.lower()
        and any(u in ln.lower() for u in ("meter", "feet", "yard"))
    ]
    assert len(data_lines) >= 3, (
        f"RED: U-FMT-01 — expected 3 data rows, got {len(data_lines)}"
    )


def test_u_fmt_02_json_format_schema(capsys):
    """U-FMT-02: format=json → [{unit,input,result}, ...] 스키마."""
    import json

    from boundary.app import run_cli_with_format

    run_cli_with_format("meter:2.5", output_format="json")
    captured = capsys.readouterr()

    parsed = json.loads(captured.out)
    assert isinstance(parsed, list), (
        f"RED: U-FMT-02 — expected JSON array, got {type(parsed)}"
    )
    assert len(parsed) >= 3, f"RED: U-FMT-02 — expected 3 rows, got {len(parsed)}"
    row = parsed[0]
    assert {"unit", "input", "result"} <= set(row.keys()), (
        f"RED: U-FMT-02 — keys unit/input/result required, got {row.keys()}"
    )


def test_u_fmt_03_csv_format_header_and_rows(capsys):
    """U-FMT-03: format=csv → unit,input,result + 3 rows."""
    from boundary.app import run_cli_with_format

    run_cli_with_format("meter:2.5", output_format="csv")
    captured = capsys.readouterr()

    lines = [ln for ln in captured.out.strip().splitlines() if ln.strip()]
    assert len(lines) >= 4, (
        f"RED: U-FMT-03 — expected header+3 rows, got {len(lines)}"
    )
    header = lines[0].lower().replace(" ", "")
    assert header == "unit,input,result", (
        f"RED: U-FMT-03 — header unit,input,result expected, got {lines[0]!r}"
    )
