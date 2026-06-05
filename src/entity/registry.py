"""Entity 단위 등록 — 동적 단위 SSOT (P1)."""

_registered: dict[str, float] = {}


def register(unit: str, meters_per_unit: float) -> None:
    """D-REG-01: 단위명 → meter 환산 비율 등록."""
    _registered[unit] = meters_per_unit


def meters_per_unit(unit: str) -> float | None:
    """등록된 단위의 meter 환산 비율, 없으면 None."""
    return _registered.get(unit)
