"""U-IN-01: 빈 입력 → 형식 오류 (E001)."""


def test_u_in_01_empty_input_format_error(capsys):
    """U-IN-01: \"\" → 형식 오류 메시지."""
    from boundary.app import run_cli

    # Given
    raw = ""

    # When
    run_cli(raw)
    captured = capsys.readouterr()
    output = (captured.out + captured.err).lower()

    # Then — Expected RED: 형식 오류 메시지 (E001)
    assert output.strip(), "RED: U-IN-01 — empty input must emit format error"
    assert "format" in output or "invalid" in output, (
        "RED: U-IN-01 — expected format error message (E001)"
    )
