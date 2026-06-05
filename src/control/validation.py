"""Control — 입력 형식·값 판정 (emit 없음)."""

from control.parse import parse_unit_value
from entity.convert import is_known_unit

E001 = "E001"
E002 = "E002"
E003 = "E003"
E004 = "E004"


def format_error_code(raw: str) -> str | None:
    """U-IN-01/02: 빈 입력·콜론 없음·값 누락 → E001."""
    if raw == "":
        return E001
    if ":" not in raw:
        return E001
    if not raw.startswith("register:"):
        _, _, value_str = raw.partition(":")
        if not value_str:
            return E001
    return None


def numeric_error_code(raw: str) -> str | None:
    """D-VAL-02: meter:hello → E002."""
    if raw.startswith("register:"):
        return None
    if ":" not in raw:
        return None
    _, _, value_str = raw.partition(":")
    if not value_str:
        return None
    try:
        float(value_str)
    except ValueError:
        return E002
    return None


def unknown_unit_error_code(raw: str) -> str | None:
    """D-VAL-03: cubit:1 (미등록) → E003."""
    if raw.startswith("register:"):
        return None
    parsed = parse_unit_value(raw)
    if parsed is None:
        return None
    unit, _ = parsed
    if not is_known_unit(unit):
        return E003
    return None


def negative_error_code(raw: str) -> str | None:
    """U-IN-03: 음수 value → E004."""
    parsed = parse_unit_value(raw)
    if parsed is None:
        return None
    _, value = parsed
    if value < 0:
        return E004
    return None
