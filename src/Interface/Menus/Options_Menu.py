
from .Base_Menu import BaseMenu
class OptionsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory_f5 = self.interface.button_factory_f5
        factory_f2_5 = self.interface.button_factory_f2_5
        self.buttons['back'] = factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2": ((50, 340), (50, 390), (10, 365)),"command1": lambda: self.change_mains({"main": 0})})
        self.buttons['visual'] = factory_f2_5.create_TextButton({"text": "Visuals","position": (self.WIDTH/2-80, self.HEIGHT/2-150),"command1": lambda: self.change_mains({"main": 5})})
        self.buttons['sound'] = factory_f2_5.create_TextButton({"text": self.interface.sound_type["sound"],"color": self.interface.sound_type["color"],"position": (self.WIDTH/2-80, self.HEIGHT/2-115),"command1": lambda: self.on_off(self.config.config_sounds, "sound_main"),"command2": self._toggle_sound,"command3": self.config.save_config})
        self.buttons['keys'] = factory_f2_5.create_TextButton({"text": "Keys","position": (self.WIDTH/2-80, self.HEIGHT/2-80),"command1": lambda: self.change_mains({"main": 6})})
        self.buttons['language'] = factory_f2_5.create_TextButton({"text": "Language","position": (self.WIDTH/2-80, self.HEIGHT/2-45)})
        self.interface.back_button = self.buttons['back']
        self.interface.visual_button = self.buttons['visual']
        self.interface.sound_button = self.buttons['sound']
        self.interface.keys_button = self.buttons['keys']
        self.interface.language_button = self.buttons['language']