import sys
from pathlib import Path
SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
for path in (PROJECT_ROOT, SRC_ROOT):
    path_str = str(path)
    if path_str not in sys.path: sys.path.insert(0, path_str)
from src.Loaders.Config_Loader import Config
from src.Events.EventManager import EventManager
from src.Game.GameLogic import GameLogic
from src.AI.AI_Controller import AIHandler
from src.Core.Interfaces.ISoundService import IAudioService
from src.Infrastructure.Container import Container
class MockAudioService(IAudioService):
    def play(self, sound_id: str, loop: bool = False) -> None: pass
    def stop(self, sound_id: str) -> None: pass
class HeadlessEnvironment:
