import pygame
from src.Core.Interfaces.ISoundService import IAudioService
class PygameAudioService(IAudioService):
    def __init__(self, asset_manager):
        self.assets = asset_manager
        self._sound_map = {
            "collision": self.assets.sound,
