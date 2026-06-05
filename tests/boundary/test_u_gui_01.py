"""U-GUI-01: PyQt GUI — meter:2.5 → 3줄 출력 (U-OUT-01 Golden Master 재사용)."""

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtCore import Qt


def test_u_gui_01_meter_25_three_lines(qtbot):
    """U-GUI-01: GUI Convert → meter/feet/yard 3줄."""
    from boundary.gui_app import UnitConverterWindow

    window = UnitConverterWindow()
    qtbot.addWidget(window)

    window.input_field.setText("meter:2.5")
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)

    from tests._approval import assert_matches_golden

    assert_matches_golden(
        window.output_display.toPlainText(), "u_out_01_meter_25.approved.txt"
    )
