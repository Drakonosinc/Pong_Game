from .Base_Menu import BaseMenu
class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['play'] = factory.create_TextButton({"text": "Press To Start","position": (self.WIDTH//2-200,self.HEIGHT//2-80),"command1":lambda:self.change_mains({"main":2})})
        self.buttons['quit'] = factory.create_TextButton({"text": "Press To Exit","position": (self.WIDTH//2-200,self.HEIGHT//2-50),"sound_touch":None,"command1": self.interface.event_quit})
        self.buttons['options'] = factory.create_TextButton({"text": "Options","position": (self.WIDTH-110,self.HEIGHT-40),"command1":lambda:self.change_mains({"main":4})})
        self.interface.play_button = self.buttons['play']
        self.interface.quit_button = self.buttons['quit']
        self.interface.options_button = self.buttons['options']
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font4.render("Space Pong", True, self.interface.WHITE),(self.WIDTH//2-245,self.HEIGHT//2-180))
        self.execute_buttons(self.buttons['play'],self.buttons['quit'],self.buttons['options'])