"""D-CNV-02 (워크북) = D-CONV-01 (FR-02): convert_all — meter → feet."""


def test_d_cnv_02_meter_to_feet():
    """D-CNV-02: 2.5 m → feet 8.20210 (5자리)."""
    from entity.constants import METER_TO_FEET, UNIT_METER
    from entity.convert import convert_all

    value = 2.5
    expected_feet = round(value * METER_TO_FEET, 5)

    result = convert_all(value, UNIT_METER)

    assert round(result["feet"], 5) == expected_feet, (
        f"RED: D-CNV-02 — expected feet {expected_feet}, got {result['feet']}"
    )
