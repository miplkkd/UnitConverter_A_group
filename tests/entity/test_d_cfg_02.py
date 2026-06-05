"""D-CFG-02 (P1 / EXT-01): load_units_config — units.json → meter 기준 비율 dict."""


def test_d_cfg_02_valid_json_loads_unit_ratios():
    """D-CFG-02: units.json — meter=1.0, feet/yard = README 비율 (그림 SSOT)."""
    from entity.config import load_units_config
    from entity.constants import METER_TO_FEET, METER_TO_YARD

    units = load_units_config("tests/fixtures/units.json")

    assert units["meter"] == 1.0
    assert units["feet"] == METER_TO_FEET, (
        f"RED: D-CFG-02 — feet must be {METER_TO_FEET}, got {units['feet']}"
    )
    assert units["yard"] == METER_TO_YARD, (
        f"RED: D-CFG-02 — yard must be {METER_TO_YARD}, got {units['yard']}"
    )
