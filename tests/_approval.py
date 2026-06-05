"""Golden Master approval — stdout vs tests/golden/*.approved.txt."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

import pytest

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def _normalize(actual: str) -> str:
    """줄 단위 고정: trailing whitespace 제거, 비어 있지 않으면 마지막 개행 1개."""
    if not actual:
        return ""
    lines = actual.splitlines()
    body = "\n".join(lines)
    return body + "\n"


def assert_matches_golden(actual: str, relative: str) -> None:
    """capsys stdout과 golden 파일 비교. UPDATE_GOLDEN=1 일 때만 갱신."""
    golden_path = GOLDEN_DIR / relative
    normalized = _normalize(actual)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(normalized, encoding="utf-8", newline="\n")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"Golden file missing: {golden_path}\n"
            f"Run: UPDATE_GOLDEN=1 python -m pytest ... to create."
        )

    expected = golden_path.read_text(encoding="utf-8")
    if expected == normalized:
        return

    diff = "\n".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            normalized.splitlines(keepends=True),
            fromfile=f"golden/{relative}",
            tofile="actual stdout",
        )
    )
    raise AssertionError(f"Golden mismatch: {relative}\n{diff}")


def assert_cli_golden(capsys, raw: str, relative: str) -> None:
    """run_cli(raw) stdout → golden matched (U-IN/U-OUT SSOT)."""
    from boundary.app import run_cli

    run_cli(raw)
    captured = capsys.readouterr()
    assert_matches_golden(captured.out, relative)


def run_gui_output(
    qtbot,
    raw: str,
    *,
    output_format: str | None = None,
    load_config: bool = False,
) -> str:
    """PyQt Convert 클릭 후 output_display plaintext (U-GUI SSOT)."""
    pytest.importorskip("PyQt6")
    from PyQt6.QtCore import Qt
    from boundary.gui_app import UnitConverterWindow

    window = UnitConverterWindow()
    qtbot.addWidget(window)

    if output_format is not None:
        index = window.format_combo.findData(output_format)
        if index >= 0:
            window.format_combo.setCurrentIndex(index)

    if load_config:
        qtbot.mouseClick(
            window.load_config_button, Qt.MouseButton.LeftButton
        )

    window.input_field.setText(raw)
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)
    return window.output_display.toPlainText()
