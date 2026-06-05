"""Boundary CLI entry — argparse --format / --config (P1 후속)."""

from __future__ import annotations

import argparse
import sys

from boundary.app import process_input_with_options
from entity.config import apply_units_config

DEFAULT_PROMPT = "Insert value for converting (ex: meter:2.5): "


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit Converter (ECB boundary)")
    parser.add_argument(
        "input",
        nargs="?",
        help="unit:value (ex: meter:2.5) or register:unit:ratio",
    )
    parser.add_argument(
        "--format",
        choices=["legacy", "table", "json", "csv"],
        default="legacy",
        help="output format (default: legacy 3-line text)",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        help="load units.json before conversion",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI main — UnitConverter.py thin wrapper target."""
    args = build_parser().parse_args(argv)

    if args.config:
        apply_units_config(args.config)

    raw = args.input
    if raw is None:
        raw = input(DEFAULT_PROMPT)

    output = process_input_with_options(raw, output_format=args.format)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
