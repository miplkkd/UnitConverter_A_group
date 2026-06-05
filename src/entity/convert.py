"""Entity layer — meter-based unit conversion (meter 경유 SSOT)."""

from entity.constants import (
    FEET_TO_METER,
    METER_TO_FEET,
    METER_TO_YARD,
    UNIT_FEET,
    UNIT_METER,
    UNIT_YARD,
    YARD_TO_METER,
)
from entity.registry import meters_per_unit


def to_meter(value: float, unit: str) -> float:
    """입력 단위·값 → meter."""
    if unit == UNIT_METER:
        return value
    if unit == UNIT_FEET:
        return value * FEET_TO_METER
    if unit == UNIT_YARD:
        return value * YARD_TO_METER
    ratio = meters_per_unit(unit)
    if ratio is not None:
        return value * ratio
    raise ValueError(f"unsupported unit: {unit}")


def convert_all(value: float, unit: str) -> dict[str, float]:
    """입력 → meter/feet/yard (meter 경유)."""
    meters = to_meter(value, unit)
    return {
        UNIT_METER: meters,
        UNIT_FEET: meters * METER_TO_FEET,
        UNIT_YARD: meters * METER_TO_YARD,
    }
