"""D-CNV-01 (워크북) = D-CONV-03: to_meter — feet → meter."""


def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    from entity.convert import to_meter

    # Given / When
    result = to_meter(1, "feet")

    # Then — Expected RED: 1 feet → 0.3048 m
    assert abs(result - 0.3048) < 1e-4, (
        f"RED: D-CNV-01 — 1 feet → 0.3048 m, got {result}"
    )
