"""Boundary CLI — control 경유 판정 · E001~E005 emit."""

from boundary.format import (
    format_conversion_lines,
    format_csv_lines,
    format_json_output,
    format_table_lines,
)
from boundary.messages import E001_FORMAT_MSG, E004_NEGATIVE_MSG
from control.convert_service import convert_input
from control.register_service import parse_register
from control.validation import E001, E004, format_error_code, negative_error_code
from entity.config import apply_units_config
from entity.registry import register as register_unit


def _handle_register(raw: str) -> str:
    try:
        unit, ratio = parse_register(raw)
    except ValueError:
        return E001_FORMAT_MSG
    register_unit(unit, ratio)
    return ""


def _resolve_output(raw: str, output_format: str = "legacy") -> str:
    if raw.startswith("register:"):
        return _handle_register(raw)

    code = format_error_code(raw)
    if code == E001:
        return E001_FORMAT_MSG
    code = negative_error_code(raw)
    if code == E004:
        return E004_NEGATIVE_MSG

    result = convert_input(raw)
    if result is None:
        return E001_FORMAT_MSG

    value, unit, converted = result
    if output_format == "table":
        return "\n".join(format_table_lines(value, unit, converted))
    if output_format == "json":
        return format_json_output(value, unit, converted)
    if output_format == "csv":
        return "\n".join(format_csv_lines(value, unit, converted))
    return "\n".join(format_conversion_lines(value, unit, converted))


def process_input(raw: str) -> str:
    """입력 처리 → CLI/GUI 공통 출력 문자열 (성공: 3줄, 오류: 1줄)."""
    return _resolve_output(raw, output_format="legacy")


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
