import unittest
from collections import defaultdict
from unittest.mock import MagicMock
import numpy as np
import pygame
from pygame.locals import *
from tests import conftest

from src.Events.EventManager import EventManager, Event
from src.Events.GameEvents import (
    QuitEvent,
    ToggleFullscreenEvent,
    PauseGameEvent,
    ResumeGameEvent,
    ChangeStateEvent,
    SaveModelEvent,
    PlayerMoveEvent,
    ChangeSpeedEvent,
    GameStateChangedEvent,
    ActionDecidedEvent,
)
from src.Events.InputHandler import InputHandler
from src.Core.Domain.DTOs import WorldStateDTO
from Utils.States import GameState


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.em = EventManager()

    def test_subscribe_and_post(self):
        received_events = []

        def on_player_move(event):
            received_events.append(event)

        self.em.subscribe(PlayerMoveEvent, on_player_move)

        move_ev = PlayerMoveEvent(player_index=1, direction=-1)
        self.em.post(move_ev)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0].player_index, 1)
        self.assertEqual(received_events[0].direction, -1)

    def test_post_only_to_matching_type(self):
        other_events = []
        self.em.subscribe(QuitEvent, lambda ev: other_events.append(ev))

        self.em.post(PlayerMoveEvent(1, 1))
        self.assertEqual(len(other_events), 0)

        self.em.post(QuitEvent())
        self.assertEqual(len(other_events), 1)

    def test_unsubscribe(self):
        calls = []
        listener = lambda ev: calls.append(ev)

        self.em.subscribe(PauseGameEvent, listener)
        self.em.post(PauseGameEvent())
        self.assertEqual(len(calls), 1)

        self.em.unsubscribe(PauseGameEvent, listener)
        self.em.post(PauseGameEvent())
        self.assertEqual(len(calls), 1)

    def test_unsubscribe_nonexistent_safely(self):
        self.em.unsubscribe(PauseGameEvent, lambda ev: None)


class TestGameEventsPayload(unittest.TestCase):
    def test_event_instantiations(self):
        q = QuitEvent()
        self.assertIsInstance(q, Event)

        tf = ToggleFullscreenEvent()
        self.assertIsInstance(tf, Event)

        cs = ChangeStateEvent({"main": GameState.PLAYING})
        self.assertEqual(cs.new_state_data["main"], GameState.PLAYING)

        pm = PlayerMoveEvent(player_index=2, direction=1, dt=0.5)
        self.assertEqual(pm.player_index, 2)
        self.assertEqual(pm.direction, 1)
        self.assertEqual(pm.dt, 0.5)

        spd = ChangeSpeedEvent(15, 1, 10, "speed_up")
        self.assertEqual(spd.fps_delta, 15)
        self.assertEqual(spd.speed_delta, 1)
        self.assertEqual(spd.limit, 10)
        self.assertEqual(spd.flag_name, "speed_up")

        dto = WorldStateDTO(0, 0, 0, 0, 0, 0)
        gs = GameStateChangedEvent(dto, player_two_reward=2.5, p1_score=3, p2_score=1)
        self.assertIs(gs.state_dto, dto)
        self.assertEqual(gs.reward, 2.5)
        self.assertEqual(gs.p1_score, 3)
        self.assertEqual(gs.p2_score, 1)

        act = ActionDecidedEvent(np.array([1, 0]))
        np.testing.assert_array_equal(act.action, [1, 0])


class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.em = EventManager()
        self.game = MagicMock()
        self.game.main = GameState.PLAYING
        self.game.speed_up = True
        self.game.speed_down = True
        self.game.running = True
        self.game.mode_game = {"Player": True, "AI": False, "Training AI": False}
        self.game.config.config_keys = {
            "UP_W": K_w,
            "DOWN_S": K_s,
            "UP_ARROW": K_UP,
            "DOWN_ARROW": K_DOWN,
        }
        self.handler = InputHandler(self.game, self.em)
        self.posted_events = []
        self.em.post = lambda ev: self.posted_events.append(ev)

    def test_keydown_fullscreen(self):
        event = pygame.event.Event(KEYDOWN, key=K_F11)
        self.handler._process_keydown_events(event)
        self.assertTrue(any(isinstance(e, ToggleFullscreenEvent) for e in self.posted_events))

    def test_keydown_pause_and_resume(self):
        event_p = pygame.event.Event(KEYDOWN, key=K_p)
        self.handler._process_keydown_events(event_p)
        self.assertTrue(any(isinstance(e, PauseGameEvent) for e in self.posted_events))

        self.posted_events.clear()
        self.game.main = GameState.PAUSE
        self.handler._process_keydown_events(event_p)
        self.assertTrue(any(isinstance(e, ResumeGameEvent) for e in self.posted_events))

    def test_keydown_speed_changes(self):
        event_plus = pygame.event.Event(KEYDOWN, key=K_KP_PLUS)
        self.handler._process_keydown_events(event_plus)
        speed_events = [e for e in self.posted_events if isinstance(e, ChangeSpeedEvent)]
        self.assertEqual(len(speed_events), 1)
        self.assertEqual(speed_events[0].fps_delta, 15)
        self.assertEqual(speed_events[0].flag_name, "speed_up")

        self.posted_events.clear()
        event_minus = pygame.event.Event(KEYDOWN, key=K_KP_MINUS)
        self.handler._process_keydown_events(event_minus)
        speed_events_minus = [e for e in self.posted_events if isinstance(e, ChangeSpeedEvent)]
        self.assertEqual(len(speed_events_minus), 1)
        self.assertEqual(speed_events_minus[0].fps_delta, -15)
        self.assertEqual(speed_events_minus[0].flag_name, "speed_down")

    def test_keydown_save_model(self):
        event_1 = pygame.event.Event(KEYDOWN, key=K_1)
        self.handler._process_keydown_events(event_1)
        self.assertTrue(any(isinstance(e, SaveModelEvent) for e in self.posted_events))

    def test_continuous_presses_player_moves(self):
        pressed = defaultdict(bool)
        pressed[K_w] = True
        pressed[K_UP] = True
        self.game.pressed_keys = pressed

        self.handler._process_continuous_presses()

        moves = [e for e in self.posted_events if isinstance(e, PlayerMoveEvent)]
        self.assertEqual(len(moves), 2)
        p1_move = next(m for m in moves if m.player_index == 1)
        self.assertEqual(p1_move.direction, -1)
        p2_move = next(m for m in moves if m.player_index == 2)
        self.assertEqual(p2_move.direction, -1)

    def test_continuous_presses_escape(self):
        pressed = defaultdict(bool)
        pressed[K_ESCAPE] = True
        self.game.pressed_keys = pressed

        self.handler._process_continuous_presses()
        self.assertFalse(self.game.running)

    def test_continuous_presses_game_over(self):
        self.game.main = GameState.GAME_OVER
        pressed = defaultdict(bool)
        pressed[K_r] = True
        self.game.pressed_keys = pressed

        self.handler._process_continuous_presses()

        state_events = [e for e in self.posted_events if isinstance(e, ChangeStateEvent)]
        self.assertEqual(len(state_events), 1)
        self.assertEqual(state_events[0].new_state_data.get("main"), GameState.PLAYING)
        self.assertTrue(state_events[0].new_state_data.get("reset"))


if __name__ == "__main__":
    unittest.main()
