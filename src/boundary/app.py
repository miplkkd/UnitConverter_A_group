"""Boundary CLI — control 경유 판정 · E001~E005 emit."""

from boundary.format import format_conversion_lines
from boundary.messages import E001_FORMAT_MSG, E004_NEGATIVE_MSG
from control.convert_service import convert_input
from control.validation import E001, E004, format_error_code, negative_error_code


def process_input(raw: str) -> str:
    """입력 처리 → CLI/GUI 공통 출력 문자열 (성공: 3줄, 오류: 1줄)."""
    code = format_error_code(raw)
    if code == E001:
        return E001_FORMAT_MSG
    code = negative_error_code(raw)
    if code == E004:
        return E004_NEGATIVE_MSG
    result = convert_input(raw)
    if result is not None:
        value, unit, converted = result
        return "\n".join(format_conversion_lines(value, unit, converted))
    return ""


def run_cli(raw: str) -> None:
    """stdin 대체 문자열 → stdout emit."""
    output = process_input(raw)
    if output:
        print(output)
