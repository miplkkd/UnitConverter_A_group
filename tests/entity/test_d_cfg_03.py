"""D-CFG-03 (P1 / EXT-01): apply_units_config — JSON → convert 비율 반영."""


def test_d_cfg_03_apply_config_enables_convert():
    """D-CFG-03: units.json apply 후 meter:2.5 → feet 8.2021 (4자리)."""
    from entity.config import apply_units_config
    from entity.convert import convert_all

    apply_units_config("tests/fixtures/units.json")
    result = convert_all(2.5, "meter")

    assert round(result["feet"], 4) == 8.2021, (
        f"RED: D-CFG-03 — feet expected 8.2021, got {result['feet']}"
    )
    assert round(result["yard"], 4) == 2.7340, (
        f"RED: D-CFG-03 — yard expected 2.7340, got {result['yard']}"
    )
