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
        
    
    
    
    
    
    
    
    
    
    
    
    