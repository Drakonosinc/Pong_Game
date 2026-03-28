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
    def __init__(self):
        self.config_loader = Config()
        self.config_loader.load_config()
        self.config = self.config_loader
        self.WIDTH = self.config.config_visuals["WIDTH"]
        self.HEIGHT = self.config.config_visuals["HEIGHT"]
        self.mode_game = {"Training AI": True, "Player": False, "AI": False}
        self.event_manager = EventManager()
        self.audio_service = MockAudioService()
        self.game_logic = GameLogic(
            self.WIDTH, 
            self.HEIGHT, 
            self.config.config_game, 
            self.mode_game, 
