"""Entity layer — meter-based unit conversion (meter 경유 SSOT)."""

from entity.config import get_active_units
from entity.constants import (
    METER_TO_FEET,
    METER_TO_YARD,
    UNIT_FEET,
    UNIT_METER,
    UNIT_YARD,
)
from entity.registry import meters_per_unit


def _meter_to_unit() -> dict[str, float]:
    active = get_active_units()
    if active:
        return {
            UNIT_METER: active.get(UNIT_METER, 1.0),
            UNIT_FEET: active.get(UNIT_FEET, METER_TO_FEET),
            UNIT_YARD: active.get(UNIT_YARD, METER_TO_YARD),
        }
    return {
        UNIT_METER: 1.0,
        UNIT_FEET: METER_TO_FEET,
        UNIT_YARD: METER_TO_YARD,
    }


def _unit_to_meter(unit: str) -> float | None:
    if unit == UNIT_METER:
        return 1.0
    ratio = _meter_to_unit().get(unit)
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
    m2u = _meter_to_unit()
    return {
        UNIT_METER: meters,
        UNIT_FEET: meters * m2u[UNIT_FEET],
        UNIT_YARD: meters * m2u[UNIT_YARD],
    }
