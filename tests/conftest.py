import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Configuración de drivers dummy para SDL
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

from src.Core.Interfaces.ISoundService import IAudioService


class DummyAudioService(IAudioService):
    def __init__(self):
        self.played_sounds = []
        self.stopped_sounds = []

    def play(self, sound_id: str, loop: bool = False) -> None:
        self.played_sounds.append((sound_id, loop))

    def stop(self, sound_id: str) -> None:
        self.stopped_sounds.append(sound_id)
