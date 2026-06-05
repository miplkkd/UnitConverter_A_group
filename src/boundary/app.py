"""Boundary CLI — control 경유 판정 · E001~E005 emit."""

from boundary.format import format_conversion_lines
from boundary.messages import E001_FORMAT_MSG, E004_NEGATIVE_MSG
from control.convert_service import convert_input
from control.validation import E001, E004, format_error_code, negative_error_code


def run_cli(raw: str) -> None:
    """stdin 대체 문자열 → stdout emit."""
    code = format_error_code(raw)
    if code == E001:
        print(E001_FORMAT_MSG)
        return
    code = negative_error_code(raw)
    if code == E004:
        print(E004_NEGATIVE_MSG)
        return
    result = convert_input(raw)
    if result is not None:
        value, unit, converted = result
        for line in format_conversion_lines(value, unit, converted):
            print(line)
