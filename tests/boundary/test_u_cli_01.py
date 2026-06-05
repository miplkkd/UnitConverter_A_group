"""U-CLI-01 (P1 후속): argparse --format / --config."""


def test_u_cli_01_argparse_format_table(capsys):
    """U-CLI-01: UnitConverter --format table meter:2.5 → table GM."""
    from boundary.cli_main import main
    from tests._approval import assert_matches_golden

    main(["meter:2.5", "--format", "table"])
    captured = capsys.readouterr()
    assert_matches_golden(
        captured.out, "u_fmt_01_table_meter_25.approved.txt"
    )


def test_u_cli_01_argparse_config_and_table(capsys):
    """U-CLI-01: --config units.json --format table."""
    from boundary.cli_main import main
    from tests._approval import assert_matches_golden

    main(["meter:2.5", "--config", "units.json", "--format", "table"])
    captured = capsys.readouterr()
    assert_matches_golden(
        captured.out, "u_fmt_01_table_meter_25.approved.txt"
    )
