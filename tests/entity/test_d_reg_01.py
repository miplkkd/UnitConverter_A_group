"""D-REG-01 (P1 / EXT-02): register — cubit 동적 등록."""


def test_d_reg_01_register_cubit():
    """D-REG-01: cubit 0.4572 m 등록 → 변환 가능."""
    from entity.registry import register
    from entity.convert import convert_all

    # Given / When
    register("cubit", 0.4572)
    result = convert_all(1, "cubit")

    # Then — Expected RED: cubit 등록 후 변환 가능
    assert abs(result["meter"] - 0.4572) < 1e-6, (
        f"RED: D-REG-01 — cubit → 0.4572 m, got {result['meter']}"
    )
