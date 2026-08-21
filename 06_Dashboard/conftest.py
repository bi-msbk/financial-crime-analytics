import sys
from pathlib import Path


DASHBOARD_ROOT = Path(__file__).resolve().parent
SRC_DIR = DASHBOARD_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
