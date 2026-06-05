"""U-CFG-01 (P1 / EXT-01): CLI — units.json 로드 후 meter:2.5 table 출력."""


def test_u_cfg_01_cli_with_config_file_table(capsys):
    """U-CFG-01: units.json + format=table → 그림과 동일 파이프 테이블."""
    from boundary.app import run_cli_with_config
    from tests._approval import assert_matches_golden

    run_cli_with_config(
        "meter:2.5",
        config_path="units.json",
        output_format="table",
    )
    captured = capsys.readouterr()

    assert_matches_golden(
        captured.out, "u_fmt_01_table_meter_25.approved.txt"
    )
