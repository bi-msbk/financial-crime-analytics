from pathlib import Path
import sys

GENERATION_SRC = Path(__file__).resolve().parents[1] / "src"

if str(GENERATION_SRC) not in sys.path:
    sys.path.insert(0, str(GENERATION_SRC))
