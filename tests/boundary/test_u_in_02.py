"""U-IN-02: 콜론 없음 → 형식 오류 (E001)."""


def test_u_in_02_meter_no_colon_format_error(capsys):
    """U-IN-02: meter → 형식 오류."""
    from tests._approval import assert_cli_golden

    assert_cli_golden(capsys, "meter", "u_in_02_no_colon.approved.txt")
