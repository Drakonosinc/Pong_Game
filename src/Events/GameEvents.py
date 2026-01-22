from .EventManager import Event
class QuitEvent(Event): pass
class ToggleFullscreenEvent(Event): pass
class PauseGameEvent(Event): pass
class ResumeGameEvent(Event): pass
class ChangeStateEvent(Event):
    def __init__(self, new_state_data: dict): self.new_state_data = new_state_data
class SaveModelEvent(Event): pass
class PlayerMoveEvent(Event):
    def __init__(self, player_index: int, direction: int, dt: float = 1.0):
        self.player_index = player_index
        self.direction = direction       
        self.dt = dt
class ChangeSpeedEvent(Event):
    def __init__(self, fps_delta, speed_delta, limit, flag_name):
        self.fps_delta = fps_delta
        self.speed_delta = speed_delta
        self.limit = limit
        self.flag_name = flag_name