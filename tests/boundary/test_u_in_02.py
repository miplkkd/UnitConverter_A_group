"""U-IN-02: 콜론 없음 → 형식 오류 (E001)."""


def test_u_in_02_meter_no_colon_format_error(capsys):
    """U-IN-02: meter → 형식 오류."""
    from boundary.app import run_cli

    # Given
    raw = "meter"

    # When
    run_cli(raw)
    captured = capsys.readouterr()

    # Then — Golden Master: 콜론 없음 E001 stdout SSOT
    from tests._approval import assert_matches_golden

    assert_matches_golden(captured.out, "u_in_02_no_colon.approved.txt")
