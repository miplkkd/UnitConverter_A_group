"""D-VAL-02 (FR-06): numeric_error_code — meter:hello → E002."""


def test_d_val_02_non_numeric_value_returns_e002():
    """D-VAL-02: 비숫자 value → E002."""
    from control.validation import E002, numeric_error_code

    assert numeric_error_code("meter:hello") == E002
    assert numeric_error_code("meter:2.5") is None
