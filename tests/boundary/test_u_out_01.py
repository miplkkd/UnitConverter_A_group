"""U-OUT-01: meter:2.5 → meter/feet/yard 3줄 출력."""


def test_u_out_01_meter_25_three_lines(capsys):
    """U-OUT-01: meter:2.5 → 3줄 이상 출력."""
    from boundary.app import run_cli

    # Given
    raw = "meter:2.5"

    # When
    run_cli(raw)
    captured = capsys.readouterr()

    # Then — Golden Master: meter:2.5 성공 stdout 3줄 SSOT
    from tests._approval import assert_matches_golden

    assert_matches_golden(captured.out, "u_out_01_meter_25.approved.txt")
