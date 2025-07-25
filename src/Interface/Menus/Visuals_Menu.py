from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory_f5 = self.interface.button_factory_f5
        factory_f2_5 = self.interface.button_factory_f2_5
        self.buttons['back'] = factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2": ((50, 340), (50, 390), (10, 365)),"command1": lambda: self.change_mains({"main": 4})})
        self.buttons['decrease_width'] = factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-200, self.HEIGHT/2-200),"command1": lambda: self._change_items("WIDTH", number=-10)})
        self.buttons['increase_width'] = factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2-40, self.HEIGHT/2-200),"command1": lambda: self._change_items("WIDTH", number=10)})
        self.buttons['decrease_height'] = factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2+20, self.HEIGHT/2-200),"command1": lambda: self._change_items("HEIGHT", number=-10)})
        self.buttons['increase_height'] = factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+200, self.HEIGHT/2-200),"command1": lambda: self._change_items("HEIGHT", number=10)})
        self.buttons['decrease_planet'] = factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-40, self.HEIGHT/2-22),"command1": lambda: self._change_items("value_planet", "planets", -1)})
        self.buttons['increase_planet'] = factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+20, self.HEIGHT/2-22),"command1": lambda: self._change_items("value_planet", "planets", 1)})
        self.buttons['decrease_back'] = factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-80, self.HEIGHT/2+160),"command1": lambda: self._change_items("value_background", "image_background", -1)})
        self.buttons['increase_back'] = factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+65, self.HEIGHT/2+160),"command1": lambda: self._change_items("value_background", "image_background", 1)})
        self.buttons['decrease_player1'] = factory_f2_5.create_TextButton({"font": self.interface.font3_5,"text": "Λ","position": (self.WIDTH/2-330, self.HEIGHT/2-120),"command1": lambda: self._change_items("value_spacecraft1", "spacecrafts", -1)})
        self.buttons['increase_player1'] = factory_f2_5.create_TextButton({"font": self.interface.font3_8,"text": "v","position": (self.WIDTH/2-330, self.HEIGHT/2+50),"command1": lambda: self._change_items("value_spacecraft1", "spacecrafts", 1)})
        self.buttons['decrease_player2'] = factory_f2_5.create_TextButton({"font": self.interface.font3_5,"text": "Λ","position": (self.WIDTH/2+310, self.HEIGHT/2-120),"command1": lambda: self._change_items("value_spacecraft2", "spacecrafts", -1)})
        self.buttons['increase_player2'] = factory_f2_5.create_TextButton({"font": self.interface.font3_8,"text": "v","position": (self.WIDTH/2+310, self.HEIGHT/2+50),"command1": lambda: self._change_items("value_spacecraft2", "spacecrafts", 1)})
        self.buttons['save_visual'] = factory_f5.create_TextButton({"text": "Save Config","position": (self.WIDTH/2+200, self.HEIGHT/2+140),"command1": self.config.save_config})
        self.buttons['default_visual'] = factory_f5.create_TextButton({"text": "Default config","position": (self.WIDTH/2+160, self.HEIGHT/2+160),"command1": lambda: self.config.config(visuals=True),"command2": self.interface.config_screen})
    def render(self):
        self.screen.blit(self.interface.image, (0, 0))
        self.screen.blit(self.interface.font2_5.render("WIDTH", True, self.interface.SKYBLUE),(self.WIDTH/2-163, self.HEIGHT/2-200))
        self.screen.blit(self.interface.font2_5.render("HEIGHT", True, self.interface.SKYBLUE),(self.WIDTH/2+60, self.HEIGHT/2-200))
        self.screen.blit(self.interface.font2_5.render("IMAGE", True, self.interface.SKYBLUE),(self.WIDTH/2-52, self.HEIGHT/2+160))
        self.interface.images_elements()
        self.execute_buttons(*self.buttons.values())
    def _change_items(self, item, background=None, number=0):
        if background is not None:
            current_value = self.config.config_visuals[item]
            options_length = len(self.config.config_visuals[background])
            self.config.config_visuals[item] = (current_value + number) % options_length
        else:self.config.config_visuals[item] = self.config.config_visuals[item] + number
        self.interface.config_screen()