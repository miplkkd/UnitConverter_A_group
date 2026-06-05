"""Control — unit:value 파싱 SSOT (emit 없음)."""


def parse_unit_value(raw: str) -> tuple[str, float] | None:
    """`unit:value` → (unit, value). 콜론 뒤 없음·비숫자 → None."""
    unit, _, value_str = raw.partition(":")
    if not value_str:
        return None
    try:
        return unit, float(value_str)
    except ValueError:
        return None
