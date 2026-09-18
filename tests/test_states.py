import unittest
from unittest.mock import MagicMock
from tests import conftest

from src.States.StateManager import StateManager
from src.States.StateFactory import StateFactory
from src.States.State import State
from Utils.States import GameState


class MockCustomState(State):
    def __init__(self, game):
        super().__init__(game)
        self.entered = False
        self.exited = False
        self.updated_with = None
        self.drawn = False
        self.handled_events = []
        self.params = None

    def enter(self, params=None):
        self.entered = True
        self.params = params

    def exit(self):
        self.exited = True

    def update(self, dt):
        self.updated_with = dt

    def draw(self, surface):
        self.drawn = True

    def handle_event(self, event):
        self.handled_events.append(event)


class TestStateManagerAndFactory(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.state_manager = None
        self.factory = StateFactory(self.mock_game)
        self.manager = StateManager(self.factory)
        self.mock_game.state_manager = self.manager

    def test_state_factory_instantiates_all_states(self):
        # Verify every GameState enum produces a valid State instance
        for state_enum in GameState:
            state_instance = self.factory.get_state(state_enum)
            self.assertIsNotNone(state_instance, f"StateFactory returned None for {state_enum}")
            self.assertIsInstance(state_instance, State)
            self.assertIs(state_instance.game, self.mock_game)

    def test_state_manager_transitions_and_lifecycles(self):
        # Custom mock state factory
        custom_state1 = MockCustomState(self.mock_game)
        custom_state2 = MockCustomState(self.mock_game)

        mock_factory = MagicMock()
        mock_factory.get_state.side_effect = lambda s: custom_state1 if s == GameState.MENU else custom_state2

        manager = StateManager(mock_factory)

        # Initial transition
        manager.change_state(GameState.MENU, params={"init": True})
        self.assertTrue(custom_state1.entered)
        self.assertEqual(custom_state1.params, {"init": True})
        self.assertEqual(len(manager.stack), 1)

        # Update and Draw delegation
        manager.update(0.016)
        self.assertEqual(custom_state1.updated_with, 0.016)

        dummy_surface = object()
        manager.draw(dummy_surface)
        self.assertTrue(custom_state1.drawn)

        dummy_event = object()
        manager.handle_event(dummy_event)
        self.assertEqual(custom_state1.handled_events, [dummy_event])

        # Change state pops and exits previous state, enters new state
        manager.change_state(GameState.PLAYING, params={"level": 1})
        self.assertTrue(custom_state1.exited)
        self.assertTrue(custom_state2.entered)
        self.assertEqual(custom_state2.params, {"level": 1})
        self.assertEqual(len(manager.stack), 1)

    def test_push_and_pop_state(self):
        s1 = MockCustomState(self.mock_game)
        s2 = MockCustomState(self.mock_game)

        mock_factory = MagicMock()
        mock_factory.get_state.side_effect = lambda s: s1 if s == GameState.PLAYING else s2

        manager = StateManager(mock_factory)

        manager.push_state(GameState.PLAYING)
        self.assertEqual(len(manager.stack), 1)

        manager.push_state(GameState.PAUSE)
        self.assertEqual(len(manager.stack), 2)
        self.assertTrue(s2.entered)

        popped = manager.pop_state()
        self.assertIs(popped, s2)
        self.assertTrue(s2.exited)
        self.assertEqual(len(manager.stack), 1)


if __name__ == "__main__":
    unittest.main()
