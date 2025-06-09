
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
        