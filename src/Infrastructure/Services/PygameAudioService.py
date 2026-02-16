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
    def play(self, sound_id: str, loop: bool = False) -> None:
        sound = self._sound_map.get(sound_id)
        if sound:
            loops = -1 if loop else 0
            sound.play(loops=loops)
        else: print(f"[AudioService] Warning: Sound ID '{sound_id}' not found.")
    def stop(self, sound_id: str) -> None:
        sound = self._sound_map.get(sound_id)
        if sound: sound.stop()