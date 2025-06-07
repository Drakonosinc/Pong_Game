from .Base_Menu import BaseMenu
class Pause(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['exit'] = factory.create_TextButton({"text": "Exit","color": self.interface.GRAY,"position": (self.WIDTH/2-40, self.HEIGHT/2-15),"color2": self.interface.SKYBLUE,"sound_touch": None,"command1": self.interface.event_quit})
        
    def render(self):pass