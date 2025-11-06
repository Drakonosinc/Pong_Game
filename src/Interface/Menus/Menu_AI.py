from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.config_buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":0})})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.execute_buttons(self.buttons['back'])