"""Control — 입력 파싱·변환 오케스트레이션 (emit 없음)."""

from entity.convert import convert_all


def convert_input(raw: str) -> tuple[float, str, dict[str, float]] | None:
    """U-OUT-01: unit:value → (value, unit, convert_all 결과)."""
    unit, _, value_str = raw.partition(":")
    if not value_str:
        return None
    try:
        value = float(value_str)
    except ValueError:
        return None
    return value, unit, convert_all(value, unit)
