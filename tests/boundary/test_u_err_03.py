"""U-ERR-03 (FR-03): cubit:1 → E003 emit."""


def test_u_err_03_unknown_unit(capsys):
    """U-ERR-03: 미등록 단위 → Unknown unit: furlong."""
    from tests._approval import assert_cli_golden

    assert_cli_golden(capsys, "furlong:1", "u_err_03_unknown_unit.approved.txt")
