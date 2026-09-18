import unittest
import numpy as np
from tests import conftest
from tests.conftest import DummyAudioService

from src.Game.GameLogic import GameLogic
from src.Events.EventManager import EventManager
from src.Events.GameEvents import (
    PlayerMoveEvent,
    ActionDecidedEvent,
    GameStateChangedEvent,
)
from src.Core.Domain.Geometry import Rectangle


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.em = EventManager()
        self.audio = DummyAudioService()
        self.config_game = {"number_balls": 2, "max_score": 5}
        self.mode_game = {"Training AI": False, "Player": True, "AI": False}
        self.logic = GameLogic(
            width=700,
            height=400,
            config_game=self.config_game,
            mode_game=self.mode_game,
            audio_service=self.audio,
            event_manager=self.em,
        )

    def test_initialization_with_multiple_balls(self):
        self.assertEqual(len(self.logic.balls), 2)
        self.assertEqual(self.logic.player_one.rect.x, 25)
        self.assertEqual(self.logic.player_two.rect.x, 665)
        self.assertEqual(len(self.logic.player_one.active), 2)

    def test_initialization_training_ai_forces_one_ball(self):
        mode_training = {"Training AI": True, "Player": False, "AI": False}
        logic_train = GameLogic(
            width=700,
            height=400,
            config_game={"number_balls": 5, "max_score": 5},
            mode_game=mode_training,
            audio_service=self.audio,
            event_manager=self.em,
        )
        self.assertEqual(len(logic_train.balls), 1)

    def test_handle_player_move_bounds(self):
        p1 = self.logic.player_one
        initial_y = p1.rect.y

        # Move UP
        self.em.post(PlayerMoveEvent(player_index=1, direction=-1))
        self.assertEqual(p1.rect.y, initial_y - 5)

        # Move DOWN
        self.em.post(PlayerMoveEvent(player_index=1, direction=1))
        self.assertEqual(p1.rect.y, initial_y)

        # Upper bound constraint (top <= 0)
        p1.rect.y = 0
        self.em.post(PlayerMoveEvent(player_index=1, direction=-1))
        self.assertEqual(p1.rect.y, 0)

        # Lower bound constraint (bottom >= height)
        p1.rect.y = 400 - p1.rect.height
        self.em.post(PlayerMoveEvent(player_index=1, direction=1))
        self.assertEqual(p1.rect.y, 400 - p1.rect.height)

    def test_handle_action_decided_discrete(self):
        p2 = self.logic.player_two
        initial_y = p2.rect.y

        # Action 0 = UP
        self.em.post(ActionDecidedEvent(action=0))
        self.assertEqual(p2.rect.y, initial_y - 5)

        # Action 1 = DOWN
        self.em.post(ActionDecidedEvent(action=1))
        self.assertEqual(p2.rect.y, initial_y)

    def test_handle_action_decided_continuous(self):
        p2 = self.logic.player_two
        initial_y = p2.rect.y

        # Positive action > 0 -> UP
        self.em.post(ActionDecidedEvent(action=np.array([0.75, -0.5])))
        self.assertEqual(p2.rect.y, initial_y - 5)

        # Negative action < 0 -> DOWN
        self.em.post(ActionDecidedEvent(action=np.array([-0.75, 0.5])))
        self.assertEqual(p2.rect.y, initial_y)

    def test_ball_exits_left_awards_player_two_score(self):
        ball = self.logic.balls[0]
        ball.rect.x = -5  # Ball exits left boundary
        initial_p2_score = self.logic.player_two.score

        self.logic.update()

        self.assertEqual(self.logic.player_two.score, initial_p2_score + 1)
        self.assertTrue(any(s[0] == "collision" for s in self.audio.played_sounds))

    def test_ball_exits_right_awards_player_one_score(self):
        ball = self.logic.balls[0]
        ball.rect.x = 690  # Ball exits right boundary >= 700 - 25 = 675
        initial_p1_score = self.logic.player_one.score

        self.logic.update()

        self.assertEqual(self.logic.player_one.score, initial_p1_score + 1)
        self.assertTrue(any(s[0] == "collision" for s in self.audio.played_sounds))

    def test_paddle_ball_collision_and_debounce(self):
        ball = self.logic.balls[0]
        p1 = self.logic.player_one

        # Place ball directly overlapping player_one
        ball.rect.x = p1.rect.x + 2
        ball.rect.y = p1.rect.y + 10
        ball.move_x = -4
        self.assertTrue(p1.active[0])

        self.logic._handle_collision(p1, ball, 0, reward=-1)

        self.assertEqual(ball.move_x, 4)
        self.assertFalse(p1.active[0])

        # Second consecutive check while still overlapping does not trigger again
        initial_reward = self.logic.player_two.reward
        self.logic._handle_collision(p1, ball, 0, reward=-1)
        self.assertEqual(self.logic.player_two.reward, initial_reward)

        # Moving ball away resets active flag
        ball.rect.x = 300
        self.logic._handle_collision(p1, ball, 0, reward=-1)
        self.assertTrue(p1.active[0])

    def test_emit_state_in_ai_mode(self):
        self.logic.mode_game["AI"] = True
        emitted_events = []
        self.em.subscribe(GameStateChangedEvent, lambda ev: emitted_events.append(ev))

        self.logic.update()

        self.assertEqual(len(emitted_events), 1)
        event = emitted_events[0]
        self.assertEqual(event.state_dto.p1_x, self.logic.player_one.rect.x)
        self.assertEqual(event.state_dto.ball_x, self.logic.balls[0].rect.x)

    def test_reset_game(self):
        self.logic.player_one.score = 3
        self.logic.player_two.score = 4
        self.logic.balls[0].rect.x = 100

        self.logic.reset_game()

        self.assertEqual(self.logic.player_one.score, 0)
        self.assertEqual(self.logic.player_two.score, 0)
        self.assertEqual(self.logic.balls[0].rect.x, self.logic.balls[0].reset_position[0])

    def test_auto_play_player1(self):
        p1 = self.logic.player_one
        self.logic.balls[0].move_y = 6
        initial_y = p1.rect.y

        self.logic.auto_play_player1()
        self.assertEqual(p1.rect.y, initial_y + 6)

        # Clamping at top
        p1.rect.y = -10
        self.logic.auto_play_player1()
        self.assertGreaterEqual(p1.rect.y, 0)

        # Clamping at bottom
        p1.rect.y = 500
        self.logic.auto_play_player1()
        self.assertLessEqual(p1.rect.y, 400 - p1.rect.height)


if __name__ == "__main__":
    unittest.main()
