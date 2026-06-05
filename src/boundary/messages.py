"""Boundary — E001~E005 메시지 SSOT (emit용)."""

E001_FORMAT_MSG = "Invalid format. Use unit:value (ex: meter:2.5)"
E004_NEGATIVE_MSG = "Negative values are not allowed"


def e002_number_message(raw: str) -> str:
    """E002: meter:hello → Invalid number: hello."""
    _, _, value_str = raw.partition(":")
    return f"Invalid number: {value_str}"


def e003_unknown_message(unit: str) -> str:
    """E003: Unknown unit: cubit."""
    return f"Unknown unit: {unit}"
