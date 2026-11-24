"""Locate the experiment and reuse the repo's pilot modules from any working directory."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = HERE / "data"
# Keep this experiment first; config/questions/client/reword come from the existing pilot.
sys.path.append(str(ROOT / "pilot"))
