"""U-GUI-02~04: PyQt GUI — E001/E004 오류 (U-IN Golden Master 재사용)."""


def test_u_gui_02_empty_input_format_error(qtbot):
    """U-GUI-02: 빈 입력 → E001."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(run_gui_output(qtbot, ""), "u_in_01_empty.approved.txt")


def test_u_gui_03_no_colon_format_error(qtbot):
    """U-GUI-03: 콜론 없음 → E001."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "meter"), "u_in_02_no_colon.approved.txt"
    )


def test_u_gui_04_negative_value_rejected(qtbot):
    """U-GUI-04: meter:-1 → E004."""
    from tests._approval import assert_matches_golden, run_gui_output

    assert_matches_golden(
        run_gui_output(qtbot, "meter:-1"), "u_in_03_negative.approved.txt"
    )
