"""Control — register:unit:ratio 파싱 (emit 없음)."""


def parse_register(raw: str) -> tuple[str, float]:
    """D-REG-02: register:cubit:0.4572 → (unit, meters_per_unit)."""
    if not raw.startswith("register:"):
        raise ValueError("not a register command")
    parts = raw.split(":")
    if len(parts) != 3 or not parts[1] or not parts[2]:
        raise ValueError("invalid register format")
    try:
        ratio = float(parts[2])
    except ValueError as exc:
        raise ValueError("invalid register ratio") from exc
    return parts[1], ratio
