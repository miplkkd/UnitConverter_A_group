"""Boundary CLI — control 경유 판정 · E001~E005 emit."""

from boundary.format import format_success_output
from boundary.messages import (
    E001_FORMAT_MSG,
    E004_NEGATIVE_MSG,
    e002_number_message,
    e003_unknown_message,
)
from control.convert_service import convert_input
from control.register_service import RegisterError, execute_register
from control.validation import (
    E001,
    E002,
    E003,
    E004,
    format_error_code,
    negative_error_code,
    numeric_error_code,
    unknown_unit_error_code,
)
from entity.config import apply_units_config


def _handle_register(raw: str) -> str:
    try:
        return execute_register(raw)
    except RegisterError:
        return E001_FORMAT_MSG


def _resolve_output(raw: str, output_format: str = "legacy") -> str:
    if raw.startswith("register:"):
        return _handle_register(raw)

    code = format_error_code(raw)
    if code == E001:
        return E001_FORMAT_MSG
    code = numeric_error_code(raw)
    if code == E002:
        return e002_number_message(raw)
    code = negative_error_code(raw)
    if code == E004:
        return E004_NEGATIVE_MSG
    code = unknown_unit_error_code(raw)
    if code == E003:
        unit, _, _ = raw.partition(":")
        return e003_unknown_message(unit)

    result = convert_input(raw)
    if result is None:
        return E001_FORMAT_MSG

    value, unit, converted = result
    return format_success_output(output_format, value, unit, converted)


def process_input(raw: str) -> str:
    """입력 처리 → CLI/GUI 공통 출력 문자열 (성공: 3줄, 오류: 1줄)."""
    return process_input_with_options(raw, output_format="legacy")


def process_input_with_options(raw: str, output_format: str = "legacy") -> str:
    """GUI/CLI — format 선택 (legacy | table | json | csv)."""
    return _resolve_output(raw, output_format=output_format)


def run_cli(raw: str) -> None:
    """stdin 대체 문자열 → stdout emit."""
    output = process_input(raw)
    if output:
        print(output)


def run_cli_with_format(raw: str, output_format: str = "table") -> None:
    """U-FMT-*: --format table | json | csv."""
    output = _resolve_output(raw, output_format=output_format)
    if output:
        print(output)


def run_cli_with_config(
    raw: str,
    config_path: str,
    output_format: str = "legacy",
) -> None:
    """U-CFG-01: units.json 로드 후 변환 출력."""
    apply_units_config(config_path)
    run_cli_with_format(raw, output_format=output_format)
