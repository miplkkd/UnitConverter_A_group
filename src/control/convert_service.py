"""Control — 입력 파싱·변환 오케스트레이션 (emit 없음)."""

from control.parse import parse_unit_value
from entity.convert import convert_all


def convert_input(raw: str) -> tuple[float, str, dict[str, float]] | None:
    """U-OUT-01: unit:value → (value, unit, convert_all 결과)."""
    parsed = parse_unit_value(raw)
    if parsed is None:
        return None
    unit, value = parsed
    return value, unit, convert_all(value, unit)
