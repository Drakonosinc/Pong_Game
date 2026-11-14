import unittest
from unittest.mock import MagicMock
import pygame
from pygame.locals import *
from tests import conftest

from pyforgeui import (
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

    def test_all_spacepong_menus_retro_modern_render(self):
        from src.Infrastructure.Container import Container
        container = Container()
        game = container.create_app()
        from src.Interface.Menus.Main_Menu import MainMenu
        from src.Interface.Menus.Game_Mode import GameMode
        from src.Interface.Menus.Options_Menu import OptionsMenu
        from src.Interface.Menus.Visuals_Menu import VisualsMenu
        from src.Interface.Menus.Menu_AI import AIMenu
        from src.Interface.Menus.Menu_Keys import KeysMenu
        from src.Interface.Menus.Pause import Pause
        from src.Interface.Menus.Game_Over import GameOver

        for menu_cls in (MainMenu, GameMode, OptionsMenu, VisualsMenu, AIMenu, KeysMenu, Pause, GameOver):
            m = menu_cls(game.ui)
            m.setup_buttons()
            m.render()

    def test_game_mode_max_score_buttons(self):
        from src.Infrastructure.Container import Container
        from src.Interface.Menus.Game_Mode import GameMode

        container = Container()
        game = container.create_app()
        gm = GameMode(game.ui)
        gm.setup_buttons()

        self.assertEqual(gm.config.config_game["max_score"], 5)

        inc_btn = gm.buttons["increase_score"]
        dec_btn = gm.buttons["decrease_score"]
        inc_pos = (inc_btn.rect.centerx, inc_btn.rect.centery)
        dec_pos = (dec_btn.rect.centerx, dec_btn.rect.centery)

        # Click increase_score (5 -> 6)
        inc_btn.pressed_button(inc_btn.rect, (True, False, False), inc_pos, draw=lambda: None, repeat=inc_btn.repeat)
        inc_btn.pressed_button(inc_btn.rect, (False, False, False), inc_pos, draw=lambda: None, repeat=inc_btn.repeat)
        self.assertEqual(gm.config.config_game["max_score"], 6)
        gm.render()

        # Click decrease_score (6 -> 5)
        dec_btn.pressed_button(dec_btn.rect, (True, False, False), dec_pos, draw=lambda: None, repeat=dec_btn.repeat)
        dec_btn.pressed_button(dec_btn.rect, (False, False, False), dec_pos, draw=lambda: None, repeat=dec_btn.repeat)
        self.assertEqual(gm.config.config_game["max_score"], 5)
        gm.render()

    def test_live_neural_network_training_background(self):
        from pyforgeai import build_model
        from src.Infrastructure.Container import Container

        container = Container()
        game = container.create_app()
        game.mode_game["Training AI"] = True
        game.game_logic.init_entities()
        model = build_model("Pytorch", input_size=6, output_size=2, hidden_sizes=[6, 6, 6, 6])
        game.model = model
        game.ai_handler.set_runtime_model(model)

        # Simulate one frame of game update + AI inference + visuals render
        game.game_logic.update()
        self.assertIsNotNone(model.layer_activations)
        self.assertEqual([len(layer) for layer in model.layer_activations], [6, 6, 6, 6, 6, 2])
        game.visuals_items.draw()


if __name__ == "__main__":
    unittest.main()
