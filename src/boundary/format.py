"""Boundary — 성공 출력 3줄 SSOT (meter/feet/yard)."""

OUTPUT_UNIT_ORDER = ("meter", "feet", "yard")


def format_conversion_lines(
    input_value: float, input_unit: str, converted: dict[str, float]
) -> list[str]:
    """입력·변환 결과 → README 형식 3줄."""
    return [
        f"{input_value} {input_unit} = {converted[unit]} {unit}"
        for unit in OUTPUT_UNIT_ORDER
    ]
