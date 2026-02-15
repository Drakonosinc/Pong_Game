import pygame
from src.Core.Interfaces.ISoundService import IAudioService
class PygameAudioService(IAudioService):
    def __init__(self, asset_manager):
        self.assets = asset_manager
        self._sound_map = {
            "collision": self.assets.sound,
            "touch": self.assets.sound_touchletters,
            "exit": self.assets.sound_exitbutton,
            "click": self.assets.sound_buttonletters}
