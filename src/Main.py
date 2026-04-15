import sys
from pathlib import Path
SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
for path in (PROJECT_ROOT, SRC_ROOT):
