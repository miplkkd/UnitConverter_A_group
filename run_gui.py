"""PyQt GUI 실행 — 프로젝트 루트에서: python run_gui.py"""

import sys
from pathlib import Path

_src = Path(__file__).resolve().parent / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from boundary.gui_app import main

if __name__ == "__main__":
    main()
