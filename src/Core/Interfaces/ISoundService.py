from abc import ABC, abstractmethod
class IAudioService(ABC):
    @abstractmethod
    def play(self, sound_id: str, loop: bool = False) -> None: pass
