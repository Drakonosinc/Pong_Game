from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        self._setup_navigation_buttons()
    def _setup_navigation_buttons(self):
        factory = self.interface.button_factory_f5
    def render(self):pass