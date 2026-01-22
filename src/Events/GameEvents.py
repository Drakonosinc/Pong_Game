from .EventManager import Event
class QuitEvent(Event): pass
class ToggleFullscreenEvent(Event): pass
class PauseGameEvent(Event): pass
class ResumeGameEvent(Event): pass
class ChangeStateEvent(Event):
    def __init__(self, new_state_data: dict): self.new_state_data = new_state_data
class SaveModelEvent(Event): pass
