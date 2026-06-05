"""U-ERR-02 (FR-06): meter:hello → E002 emit."""


def test_u_err_02_non_numeric_value(capsys):
    """U-ERR-02: 비숫자 → Invalid number: hello."""
    from tests._approval import assert_cli_golden

    assert_cli_golden(capsys, "meter:hello", "u_err_02_non_numeric.approved.txt")
