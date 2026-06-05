"""D-CONV-01 (FR-02): convert_all — meter → feet (README 3.28084, 5dp)."""


def test_d_conv_01_meter_to_feet():
    """D-CONV-01: 2.5 meter → feet 8.20210."""
    from entity.convert import convert_all

    # Given
    value = 2.5
    unit = "meter"

    # When
    result = convert_all(value, unit)

    # Then — 2.5 × 3.28084 = 8.20210 (5자리)
    assert round(result["feet"], 5) == 8.20210
