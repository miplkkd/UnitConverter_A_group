"""D-CNV-02 (워크북) = D-CONV-01 (FR-02): convert_all — meter → feet."""


def test_d_cnv_02_meter_to_feet():
    """D-CNV-02: 2.5 m → feet 8.20210 (5자리)."""
    from entity.convert import convert_all

    # Given
    value = 2.5
    unit = "meter"

    # When
    result = convert_all(value, unit)

    # Then — Expected RED: 2.5 m → feet 8.20210 (5자리)
    assert round(result["feet"], 5) == 8.20210, (
        f"RED: D-CNV-02 — expected feet 8.20210, got {result['feet']}"
    )
