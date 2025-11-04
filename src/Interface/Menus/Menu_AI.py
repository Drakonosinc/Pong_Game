from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.config_buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5