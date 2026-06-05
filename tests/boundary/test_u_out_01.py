"""U-OUT-01: meter:2.5 → meter/feet/yard 3줄 출력."""


def test_u_out_01_meter_25_three_lines(capsys):
    """U-OUT-01: meter:2.5 → 3줄 이상 출력."""
    from tests._approval import assert_cli_golden

    assert_cli_golden(capsys, "meter:2.5", "u_out_01_meter_25.approved.txt")
