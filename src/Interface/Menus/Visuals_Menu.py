
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
        