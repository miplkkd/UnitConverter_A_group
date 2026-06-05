"""D-REG-02 (P1 / EXT-02): parse_register — register:unit:ratio 파싱."""


def test_d_reg_02_parse_register_cubit():
    """D-REG-02: register:cubit:0.4572 → (cubit, 0.4572)."""
    from control.register_service import parse_register

    # Given
    raw = "register:cubit:0.4572"

    # When
    unit, ratio = parse_register(raw)

    # Then — RED: control 파싱 SSOT (emit 없음)
    assert unit == "cubit", f"RED: D-REG-02 — unit, got {unit!r}"
    assert abs(ratio - 0.4572) < 1e-9, f"RED: D-REG-02 — ratio, got {ratio}"
