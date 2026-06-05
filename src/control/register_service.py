"""Control — register:unit:ratio 파싱·오케스트레이션 (emit 없음)."""

from entity.registry import register


class RegisterError(Exception):
    """잘못된 register 형식."""


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


def execute_register(raw: str) -> str:
    """D-REG-02 orchestration: parse → entity register → 확인 메시지."""
    try:
        unit, ratio = parse_register(raw)
    except ValueError as exc:
        raise RegisterError(str(exc)) from exc
    register(unit, ratio)
    return f"Registered: {unit} ({ratio} m per unit)"
