import pygame
from pygame.locals import KEYDOWN
from .Base_Menu import BaseMenu
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.key = None
        self.key_name = None
        self.button_key = None
    def setup_buttons(self):
        factory_f5 = self.interface.button_factory_f5
        self.buttons['back'] = factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2": ((50, 340), (50, 390), (10, 365)),"command1": lambda: self.change_mains({"main": 4})})
        self.buttons['up_w'] = factory_f5.create_TextButton({"font": self.interface.font4_5,"text": self.config.config_keys["Name_key1"],"position": (self.WIDTH/2-240, self.HEIGHT/2-170),"command1": lambda: self._change_keys("UP_W", "Name_key1", self.buttons['up_w'])})
        self.buttons['down_s'] = factory_f5.create_TextButton({"font": self.interface.font4_5,"text": self.config.config_keys["Name_key2"],"position": (self.WIDTH/2-217, self.HEIGHT/2-20),"command1": lambda: self._change_keys("DOWN_S", "Name_key2", self.buttons['down_s'])})
        self.buttons['up_arrow'] = factory_f5.create_TextButton({"font": self.interface.font4_5,"text": self.config.config_keys["Name_key3"],"position": (self.WIDTH/2+200, self.HEIGHT/2-170),"command1": lambda: self._change_keys("UP_ARROW", "Name_key3", self.buttons['up_arrow'])})
        self.buttons['down_arrow'] = factory_f5.create_TextButton({"font": self.interface.font4_5,"text": self.config.config_keys["Name_key4"],"position": (self.WIDTH/2+200, self.HEIGHT/2-20),"command1": lambda: self._change_keys("DOWN_ARROW", "Name_key4", self.buttons['down_arrow'])})
        self.buttons['save'] = factory_f5.create_TextButton({"text": "Save Config","position": (self.WIDTH/2+200, self.HEIGHT/2+140),"command1": self.config.save_config})
        
    
    
    
    
    
    
    
    
    
    
    
    