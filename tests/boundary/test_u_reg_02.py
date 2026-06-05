"""U-REG-02 (P1 / EXT-02): CLI — 잘못된 register 형식 → E001."""


def test_u_reg_02_invalid_register_format_error(capsys):
    """U-REG-02: register:cubit → 형식 오류 (E001)."""
    from boundary.app import run_cli

    # Given
    raw = "register:cubit"

    # When
    run_cli(raw)
    captured = capsys.readouterr()

    # Then — RED: register 형식 오류 emit
    assert "Invalid format" in captured.out, (
        f"RED: U-REG-02 — E001 expected, got {captured.out!r}"
    )
