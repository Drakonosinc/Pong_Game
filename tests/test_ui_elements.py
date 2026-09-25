import unittest
from unittest.mock import MagicMock
import pygame
from pygame.locals import *
from tests import conftest

from src.Interface.Elements_interface import (
    ElementsFactory,
    Text,
    TextButton,
    PolygonButton,
    Input_text,
    ScrollBar,
    ComboBoxDown,
)


class TestUIElements(unittest.TestCase):
    def setUp(self):
        self.surface = pygame.Surface((700, 400))
        self.font = pygame.font.Font(None, 24)
        self.factory = ElementsFactory({
            "screen": self.surface,
            "font": self.font,
            "color": (255, 255, 255),
            "hover_color": (255, 199, 51),
        })

    def test_factory_creates_primitives(self):
        text_el = self.factory.create_Text({"text": "Hello Pong", "position": (10, 10)})
