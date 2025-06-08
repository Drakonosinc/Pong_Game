from .Base_Menu import BaseMenu
class Pause(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['exit'] = factory.create_TextButton({"text": "Exit","color": self.interface.GRAY,"position": (self.WIDTH/2-40, self.HEIGHT/2-15),"color2": self.interface.SKYBLUE,"sound_touch": None,"command1": self.interface.event_quit})
        self.buttons['reset'] = factory.create_TextButton({"text": "Reset","color": self.interface.GRAY,"position": (self.WIDTH/2-55, self.HEIGHT/2-85),"color2": self.interface.SKYBLUE,"command1": lambda: self.change_mains({"main": -1}),"command2": self.interface.reset})
        self.buttons['menu'] = factory.create_TextButton({"text": "Menu","color": self.interface.GRAY,"position": (self.WIDTH/2-45, self.HEIGHT/2-50),"color2": self.interface.SKYBLUE,"command1": lambda: self.change_mains({"main": 0, "run": True}),"command2": self.interface.reset})
        self.interface.exit_button = self.buttons['exit']
        self.interface.reset_pause_button = self.buttons['reset']
        self.interface.go_main_button = self.buttons['menu']
    def execute_buttons(self):
        for button in self.buttons.values():button.draw()
    def render(self):
        self.filt(180)
        self.screen.blit(self.interface.font3.render("Pause", True, "gray"),(self.WIDTH/2-105, self.HEIGHT/2-150))
        self.execute_buttons()