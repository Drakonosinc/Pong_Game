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
        self.assertIsInstance(text_el, Text)

        btn = self.factory.create_TextButton({
            "text": "Click Me",
            "position": (100, 100),
            "command1": lambda: None,
        })
        self.assertIsInstance(btn, TextButton)

        poly_btn = self.factory.create_PolygonButton({
            "position": [(10, 10), (30, 10), (20, 30)],
        })
        self.assertIsInstance(poly_btn, PolygonButton)

        input_txt = self.factory.create_InputText({
            "position": (200, 200, 150, 40),
        })
        self.assertIsInstance(input_txt, Input_text)

        scrollbar = self.factory.create_ScrollBar({
            "position": (300, 50, 20, 100),
        })
        self.assertIsInstance(scrollbar, ScrollBar)

        combo = self.factory.create_ComboBox({
            "text": "Select",
            "position": (400, 50),
            "options": ["Opt1", "Opt2"],
            "type_dropdown": "down",
        })
        self.assertIsInstance(combo, ComboBoxDown)

    def test_text_draw(self):
        text_el = self.factory.create_Text({"text": "Test Score: 10", "position": (20, 20)})
        text_el.draw()

    def test_text_button_command_execution(self):
        command_called = []
        btn = self.factory.create_TextButton({
            "text": "Action",
            "position": (50, 50),
            "command1": lambda: command_called.append(True),
        })

        # Simulate button press
        btn.states["presses_touch"] = True
        btn.pressed_button(
            rect=btn.rect,
            pressed_mouse=(True, False, False),
            mouse_pos=(btn.rect.centerx, btn.rect.centery),
            draw=lambda: None,
        )
        self.assertTrue(btn.states["active"])

        # Release mouse over button triggers command
        btn.pressed_button(
            rect=btn.rect,
            pressed_mouse=(False, False, False),
            mouse_pos=(btn.rect.centerx, btn.rect.centery),
            draw=lambda: None,
        )
        self.assertEqual(len(command_called), 1)

    def test_input_text_typing_and_backspace(self):
        input_txt = self.factory.create_InputText({
            "position": (10, 10, 100, 30),
        })
        input_txt.states["active"] = True

        # Type 'A'
        ev_a = pygame.event.Event(KEYDOWN, key=K_a, unicode="A")
        input_txt.change_text(ev_a)
        self.assertEqual(input_txt.text, "A")

        # Type 'B'
        ev_b = pygame.event.Event(KEYDOWN, key=K_b, unicode="B")
        input_txt.change_text(ev_b)
        self.assertEqual(input_txt.text, "AB")

        # Backspace deletes 'B'
        ev_back = pygame.event.Event(KEYDOWN, key=K_BACKSPACE, unicode="")
        input_txt.change_text(ev_back)
        self.assertEqual(input_txt.text, "A")


if __name__ == "__main__":
    unittest.main()
