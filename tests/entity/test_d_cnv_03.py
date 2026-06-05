"""D-CNV-03 (워크북) = D-CONV-05: convert_all — feet→yard, meter 경유 일치."""


def test_d_cnv_03_feet_yard_via_meter():
    """D-CNV-03: feet→yard 변환은 meter 경유만 (직접 비율 금지)."""
    from entity.convert import convert_all, to_meter

    # Given
    value = 1
    unit = "feet"

    # When — convert_all vs to_meter 경유 yard
    via_convert_all = convert_all(value, unit)["yard"]
    meters = to_meter(value, unit)
    via_meter = convert_all(meters, "meter")["yard"]

    # Then — Expected RED: feet→yard meter 경유 일치
    assert abs(via_convert_all - via_meter) < 1e-9, (
        f"RED: D-CNV-03 — meter path mismatch: {via_convert_all} vs {via_meter}"
    )
