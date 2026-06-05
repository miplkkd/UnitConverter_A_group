"""U-GUI-05~09 (P1): PyQt smoke — format · config · register."""

import pytest


def test_u_gui_05_table_format_pipe_table(qtbot):
    """U-GUI-05: format=table → pipe table GM (U-FMT-01)."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "meter:2.5", output_format="table"),
        "u_fmt_01_table_meter_25.approved.txt",
    )


def test_u_gui_06_config_load_then_table(qtbot):
    """U-GUI-06: Load units.json + table → GM (U-CFG-01)."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(
            qtbot,
            "meter:2.5",
            output_format="table",
            load_config=True,
        ),
        "u_fmt_01_table_meter_25.approved.txt",
    )


def test_u_gui_07_register_then_convert_cubit(qtbot):
    """U-GUI-07: register → cubit:1 (U-REG-01)."""
    pytest.importorskip("PyQt6")
    from PyQt6.QtCore import Qt
    from boundary.gui_app import UnitConverterWindow

    window = UnitConverterWindow()
    qtbot.addWidget(window)

    window.input_field.setText("register:cubit:0.4572")
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)
    register_out = window.output_display.toPlainText()
    assert "Registered" in register_out and "cubit" in register_out

    window.input_field.setText("cubit:1")
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)
    convert_out = window.output_display.toPlainText()

    assert "0.4572" in convert_out or "0.457" in convert_out
    assert "meter" in convert_out


def test_u_gui_08_json_format_schema(qtbot):
    """U-GUI-08: format=json → [{unit,input,result}] (U-FMT-02)."""
    import json

    from tests._approval import run_gui_output

    parsed = json.loads(run_gui_output(qtbot, "meter:2.5", output_format="json"))
    assert isinstance(parsed, list)
    assert len(parsed) >= 3
    assert {"unit", "input", "result"} <= set(parsed[0].keys())


def test_u_gui_09_csv_format_header_and_rows(qtbot):
    """U-GUI-09: format=csv → unit,input,result (U-FMT-03)."""
    from tests._approval import run_gui_output

    out = run_gui_output(qtbot, "meter:2.5", output_format="csv")
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    assert len(lines) >= 4
    assert lines[0].lower().replace(" ", "") == "unit,input,result"


def test_u_gui_10_non_numeric_value_e002(qtbot):
    """U-GUI-10: meter:hello → E002 GM (U-ERR-02)."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "meter:hello"),
        "u_err_02_non_numeric.approved.txt",
    )


def test_u_gui_11_unknown_unit_e003(qtbot):
    """U-GUI-11: furlong:1 → E003 GM (U-ERR-03)."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "furlong:1"),
        "u_err_03_unknown_unit.approved.txt",
    )
