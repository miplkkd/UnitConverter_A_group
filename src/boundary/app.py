"""Boundary CLI — control 경유 판정 · E001~E005 emit."""

from boundary.messages import E001_FORMAT_MSG
from control.validation import E001, format_error_code


def run_cli(raw: str) -> None:
    """stdin 대체 문자열 → stdout emit."""
    code = format_error_code(raw)
    if code == E001:
        print(E001_FORMAT_MSG)
