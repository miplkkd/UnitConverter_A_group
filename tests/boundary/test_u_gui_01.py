"""U-GUI-01: PyQt GUI — meter:2.5 → 3줄 출력 (U-OUT-01 Golden Master 재사용)."""


def test_u_gui_01_meter_25_three_lines(qtbot):
    """U-GUI-01: GUI Convert → meter/feet/yard 3줄."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "meter:2.5"), "u_out_01_meter_25.approved.txt"
    )
