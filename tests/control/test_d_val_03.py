"""D-VAL-03 (FR-03): unknown_unit_error_code — cubit:1 → E003."""


def test_d_val_03_unregistered_unit_returns_e003():
    """D-VAL-03: 미등록 단위 → E003."""
    from control.validation import E003, unknown_unit_error_code

    assert unknown_unit_error_code("furlong:1") == E003
    assert unknown_unit_error_code("meter:2.5") is None
