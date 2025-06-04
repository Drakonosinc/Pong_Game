from .Base_Menu import BaseMenu
class GameOver(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['main'] = factory.create_TextButton({"text": "Main Menu Press E","color": self.interface.BLACK,"position": (self.WIDTH/2-166,self.HEIGHT/2-110),"command1":lambda:self.change_mains({"main":0,"run":True})})
        self.buttons['reset'] = factory.create_TextButton({"text": "Reset Press R","color": self.interface.BLACK,"position": (self.WIDTH/2-130,self.HEIGHT/2-80),"command1": self.interface.reset,"command2":lambda:self.change_mains({"main":-1})})
    def render(self):pass