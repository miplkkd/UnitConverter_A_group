"""UnitConverter — ECB boundary thin wrapper (legacy entry point)."""

import sys
from pathlib import Path

_src = Path(__file__).resolve().parent / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from boundary.cli_main import main

if __name__ == "__main__":
    raise SystemExit(main())
