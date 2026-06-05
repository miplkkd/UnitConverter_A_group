"""U-IN-03: 음수 → 거부 (E004)."""


def test_u_in_03_negative_value_rejected(capsys):
    """U-IN-03: meter:-1 → 음수 거부."""
    from boundary.app import run_cli

    # Given
    raw = "meter:-1"

    # When
    run_cli(raw)
    captured = capsys.readouterr()

    # Then — Golden Master: 음수 E004 stdout SSOT
    from tests._approval import assert_matches_golden

    assert_matches_golden(captured.out, "u_in_03_negative.approved.txt")
