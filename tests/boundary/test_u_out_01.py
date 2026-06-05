"""U-OUT-01: meter:2.5 → meter/feet/yard 3줄 출력."""


def test_u_out_01_meter_25_three_lines(capsys):
    """U-OUT-01: meter:2.5 → 3줄 이상 출력."""
    from boundary.app import run_cli

    # Given
    raw = "meter:2.5"

    # When
    run_cli(raw)
    captured = capsys.readouterr()
    lines = [ln for ln in captured.out.splitlines() if ln.strip()]

    # Then — Expected RED: 3줄 이상 출력 (meter/feet/yard)
    assert len(lines) >= 3, (
        f"RED: U-OUT-01 — expected 3+ output lines, got {len(lines)}"
    )
