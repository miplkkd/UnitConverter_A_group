"""Entity layer — meter-based unit conversion."""

from entity.constants import (
    METER_TO_FEET,
    METER_TO_YARD,
    UNIT_FEET,
    UNIT_METER,
    UNIT_YARD,
)


def convert_all(value: float, unit: str) -> dict[str, float]:
    """Convert value from unit to meter, feet, and yard."""
    if unit == UNIT_METER:
        meters = value
    else:
        raise ValueError(f"unsupported unit: {unit}")

    return {
        UNIT_METER: meters,
        UNIT_FEET: meters * METER_TO_FEET,
        UNIT_YARD: meters * METER_TO_YARD,
    }
