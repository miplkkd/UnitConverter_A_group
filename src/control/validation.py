"""Control — 입력 형식·값 판정 (emit 없음)."""

E001 = "E001"
E004 = "E004"


def format_error_code(raw: str) -> str | None:
    """U-IN-01: 빈 입력 → E001. U-IN-02: 콜론 없음 → E001."""
    if raw == "":
        return E001
    if ":" not in raw:
        return E001
    return None


def negative_error_code(raw: str) -> str | None:
    """U-IN-03: 음수 value → E004."""
    _, _, value_part = raw.partition(":")
    if not value_part:
        return None
    try:
        value = float(value_part)
    except ValueError:
        return None
    if value < 0:
        return E004
    return None
