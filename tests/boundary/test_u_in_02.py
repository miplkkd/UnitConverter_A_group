"""U-IN-02: 콜론 없음 → 형식 오류 (E001)."""


def test_u_in_02_meter_no_colon_format_error(capsys):
    """U-IN-02: meter → 형식 오류."""
    from boundary.app import run_cli

    # Given
    raw = "meter"

    # When
    run_cli(raw)
    captured = capsys.readouterr()
    output = (captured.out + captured.err).lower()

    # Then — Expected RED: 형식 오류 (E001)
    assert output.strip(), "RED: U-IN-02 — missing colon must emit format error"
    assert "format" in output or "invalid" in output or ":" in output, (
        "RED: U-IN-02 — expected format error for 'meter' without colon"
    )
