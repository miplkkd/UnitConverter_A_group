"""Boundary — 성공 출력 SSOT (legacy 3줄 · table · json · csv)."""

import json

OUTPUT_UNIT_ORDER = ("meter", "feet", "yard")


def format_conversion_lines(
    input_value: float, input_unit: str, converted: dict[str, float]
) -> list[str]:
    """입력·변환 결과 → README 형식 3줄."""
    return [
        f"{input_value} {input_unit} = {converted[unit]} {unit}"
        for unit in OUTPUT_UNIT_ORDER
    ]


def _format_input_cell(value: float) -> str:
    text = f"{value:g}"
    return text


def _format_result_cell(
    input_value: float, input_unit: str, unit: str, converted: float
) -> str:
    if unit == input_unit:
        return _format_input_cell(input_value)
    return f"{round(converted, 4):.4f}"


def format_table_lines(
    input_value: float, input_unit: str, converted: dict[str, float]
) -> list[str]:
    """U-FMT-01: pipe table — | unit | input | result |."""
    lines = [
        "| unit  | input | result |",
        "|-------|-------|--------|",
    ]
    for unit in OUTPUT_UNIT_ORDER:
        inp = _format_input_cell(input_value)
        res = _format_result_cell(input_value, input_unit, unit, converted[unit])
        lines.append(f"| {unit:<5} | {inp:<5} | {res:<6} |")
    return lines


def format_json_output(
    input_value: float, input_unit: str, converted: dict[str, float]
) -> str:
    """U-FMT-02: [{unit,input,result}, ...]."""
    rows = [
        {
            "unit": unit,
            "input": input_value,
            "result": converted[unit],
        }
        for unit in OUTPUT_UNIT_ORDER
    ]
    return json.dumps(rows)


def format_csv_lines(
    input_value: float, input_unit: str, converted: dict[str, float]
) -> list[str]:
    """U-FMT-03: unit,input,result + data rows."""
    lines = ["unit,input,result"]
    for unit in OUTPUT_UNIT_ORDER:
        res = _format_result_cell(input_value, input_unit, unit, converted[unit])
        inp = _format_input_cell(input_value)
        lines.append(f"{unit},{inp},{res}")
    return lines

