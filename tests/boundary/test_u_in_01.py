"""U-IN-01: 빈 입력 → 형식 오류 (E001)."""


def test_u_in_01_empty_input_format_error(capsys):
    """U-IN-01: \"\" → 형식 오류 메시지."""
    from boundary.app import run_cli

    # Given
    raw = ""

    # When
    run_cli(raw)
    captured = capsys.readouterr()

    # Then — Golden Master: 빈 입력 E001 stdout SSOT
    from tests._approval import assert_matches_golden

    assert_matches_golden(captured.out, "u_in_01_empty.approved.txt")
