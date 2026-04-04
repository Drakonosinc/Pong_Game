import pygame
from .Elements_interface import *
from Interface.Menus.Base_Menu import BaseMenu 
from Events.GameEvents import QuitEvent
from Loaders.AILoader import AILoader
class Interface(BaseMenu):
    def __init__(self, context):
        self.context = context
        self.game = None
