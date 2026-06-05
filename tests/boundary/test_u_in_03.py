"""U-IN-03: 음수 → 거부 (E004)."""


def test_u_in_03_negative_value_rejected(capsys):
    """U-IN-03: meter:-1 → 음수 거부."""
    from boundary.app import run_cli

    # Given
    raw = "meter:-1"

    # When
    run_cli(raw)
    captured = capsys.readouterr()
    output = captured.out + captured.err
    success_lines = [ln for ln in captured.out.splitlines() if ln.strip()]

    # Then — Expected RED: 음수 거부 (3줄 성공 출력 아님)
    assert len(success_lines) < 3, (
        "RED: U-IN-03 — negative input must not produce 3-line conversion output"
    )
    assert output.strip(), "RED: U-IN-03 — negative input must emit rejection message"
    lower = output.lower()
    assert (
        "negative" in lower
        or "invalid" in lower
        or "error" in lower
        or len(success_lines) == 0
    ), "RED: U-IN-03 — expected negative rejection (E004)"
