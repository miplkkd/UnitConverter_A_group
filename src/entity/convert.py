"""Entity layer — meter-based unit conversion (meter 경유 SSOT)."""

from entity.config import get_meter_to_unit_ratios
from entity.constants import UNIT_FEET, UNIT_METER, UNIT_YARD
from entity.registry import meters_per_unit


def is_known_unit(unit: str) -> bool:
    """D-VAL-03: built-in 또는 registry 등록 단위."""
    if unit in (UNIT_METER, UNIT_FEET, UNIT_YARD):
        return True
    return meters_per_unit(unit) is not None


def _unit_to_meter(unit: str) -> float | None:
    if unit == UNIT_METER:
        return 1.0
    ratio = get_meter_to_unit_ratios().get(unit)
    if ratio is not None and ratio != 0:
        return 1.0 / ratio
    return None


def to_meter(value: float, unit: str) -> float:
    """입력 단위·값 → meter."""
    u2m = _unit_to_meter(unit)
    if u2m is not None:
        return value * u2m
    ratio = meters_per_unit(unit)
    if ratio is not None:
        return value * ratio
    raise ValueError(f"unsupported unit: {unit}")


def convert_all(value: float, unit: str) -> dict[str, float]:
    """입력 → meter/feet/yard (meter 경유)."""
    meters = to_meter(value, unit)
    m2u = get_meter_to_unit_ratios()
    return {
        UNIT_METER: meters,
        UNIT_FEET: meters * m2u[UNIT_FEET],
        UNIT_YARD: meters * m2u[UNIT_YARD],
    }
