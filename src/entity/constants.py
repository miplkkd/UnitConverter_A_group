"""MagicConstant SSOT — conversion ratios and unit names."""

UNIT_METER = "meter"
UNIT_FEET = "feet"
UNIT_YARD = "yard"

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361

FEET_TO_METER = 1 / METER_TO_FEET
YARD_TO_METER = 1 / METER_TO_YARD

DEFAULT_UNIT_RATIOS: dict[str, float] = {
    UNIT_METER: 1.0,
    UNIT_FEET: METER_TO_FEET,
    UNIT_YARD: METER_TO_YARD,
}
