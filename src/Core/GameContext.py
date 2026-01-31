class GameContext:
    def __init__(self, config, assets, event_manager, window_manager):
        self.config = config
        self.assets = assets
        self.event_manager = event_manager
        self.window_manager = window_manager
        self.sound = assets