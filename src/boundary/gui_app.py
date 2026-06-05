"""Boundary PyQt GUI — control 경유 · E001~E004 emit (CLI와 동일 SSOT)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from boundary.app import process_input


class UnitConverterWindow(QMainWindow):
    """unit:value 입력 → 변환 결과 또는 오류 메시지 표시."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setMinimumWidth(520)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

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

    def _on_convert(self) -> None:
        self.output_display.setPlainText(process_input(self.input_field.text()))

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
