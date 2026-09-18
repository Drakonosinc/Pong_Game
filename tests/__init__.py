import os
import sys
from pathlib import Path

# Configurar drivers simulados para pygame en modo headless
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

import pygame
if not pygame.get_init():
    pygame.init()

# Sincronizar alias de módulos para evitar duplicación entre "src.X" y "X"
import src.Utils.States
sys.modules["Utils"] = sys.modules.get("src.Utils")
sys.modules["Utils.States"] = sys.modules.get("src.Utils.States")
