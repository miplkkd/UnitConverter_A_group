"""Boundary PyQt GUI — control 경유 · E001~E004 emit (CLI와 동일 SSOT)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from boundary.app import process_input_with_options
from entity.config import apply_units_config

OUTPUT_FORMATS: tuple[tuple[str, str], ...] = (
    ("legacy", "legacy (3 lines)"),
    ("table", "table"),
    ("json", "json"),
    ("csv", "csv"),
)

DEFAULT_CONFIG_PATH = "units.json"


class UnitConverterWindow(QMainWindow):
    """unit:value 입력 → 변환 결과 또는 오류 메시지 표시."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setMinimumWidth(560)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        options_row = QHBoxLayout()
        options_row.addWidget(QLabel("Output format:"))
        self.format_combo = QComboBox()
        self.format_combo.setObjectName("format_combo")
        for key, label in OUTPUT_FORMATS:
            self.format_combo.addItem(label, key)
        options_row.addWidget(self.format_combo)

        self.load_config_button = QPushButton("Load units.json")
        self.load_config_button.setObjectName("load_config_button")
        self.load_config_button.clicked.connect(self._on_load_config)
        options_row.addWidget(self.load_config_button)
        layout.addLayout(options_row)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Input (unit:value):"))
        self.input_field = QLineEdit()
        self.input_field.setObjectName("input_field")
        self.input_field.setPlaceholderText("meter:2.5")
        input_row.addWidget(self.input_field)
        layout.addLayout(input_row)

        self.convert_button = QPushButton("Convert")
        self.convert_button.setObjectName("convert_button")
        self.convert_button.clicked.connect(self._on_convert)
        layout.addWidget(self.convert_button)

        self.output_display = QTextEdit()
        self.output_display.setObjectName("output_display")
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        self.input_field.returnPressed.connect(self._on_convert)

    def _current_format(self) -> str:
        data = self.format_combo.currentData()
        return data if isinstance(data, str) else "legacy"

    def _on_load_config(self) -> None:
        apply_units_config(DEFAULT_CONFIG_PATH)
        self.output_display.setPlainText(f"Config loaded: {DEFAULT_CONFIG_PATH}")

    def _on_convert(self) -> None:
        output = process_input_with_options(
            self.input_field.text(),
            output_format=self._current_format(),
        )
        self.output_display.setPlainText(output)

    def run_convert(self) -> None:
        """테스트·자동화용 — Convert 버튼과 동일."""
        self._on_convert()


def main() -> None:
    app = QApplication(sys.argv)
    window = UnitConverterWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
