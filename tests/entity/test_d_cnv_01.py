"""D-CNV-01 (워크북) = D-CONV-03: to_meter — feet → meter."""


def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    from entity.constants import FEET_TO_METER
    from entity.convert import to_meter

    result = to_meter(1, "feet")

    assert abs(result - FEET_TO_METER) < 1e-4, (
        f"RED: D-CNV-01 — 1 feet → {FEET_TO_METER} m, got {result}"
    )
