"""U-REG-01 (P1 / EXT-02): CLI 동적 등록 → cubit:1 즉시 변환."""


def test_u_reg_01_register_then_convert_cubit(capsys):
    """U-REG-01: register:cubit:0.4572 후 cubit:1 → meter 줄 포함."""
    from boundary.app import run_cli

    # Given / When — register then convert
    try:
        run_cli("register:cubit:0.4572")
        run_cli("cubit:1")
    except ValueError as exc:
        raise AssertionError(
            f"RED: U-REG-01 — register CLI not wired, got {exc}"
        ) from exc
    captured = capsys.readouterr()

    # Then — RED: 1 cubit = 0.4572 m
    assert "0.4572" in captured.out or "0.457" in captured.out, (
        f"RED: U-REG-01 — cubit conversion missing in {captured.out!r}"
    )
    assert "meter" in captured.out, "RED: U-REG-01 — meter line missing"
