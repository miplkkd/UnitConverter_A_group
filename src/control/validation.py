"""Control — 입력 형식 판정 (emit 없음)."""

E001 = "E001"


def format_error_code(raw: str) -> str | None:
    """U-IN-01: 빈 입력 → E001."""
    if raw == "":
        return E001
    return None
