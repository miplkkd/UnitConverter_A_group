"""U-IN-03: 음수 → 거부 (E004)."""


def test_u_in_03_negative_value_rejected(capsys):
    """U-IN-03: meter:-1 → 음수 거부."""
    from tests._approval import assert_cli_golden

    assert_cli_golden(capsys, "meter:-1", "u_in_03_negative.approved.txt")
