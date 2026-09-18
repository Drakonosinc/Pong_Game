import unittest
from tests import conftest

from src.Entities.Players import Player
from src.Entities.Balls import Ball
from src.Core.Domain.Geometry import Rectangle


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(x=25, y=150, width=11, height=90, active=[True, True])

    def test_initialization(self):
        self.assertEqual(self.player.rect.x, 25)
        self.assertEqual(self.player.rect.y, 150)
        self.assertEqual(self.player.rect.width, 11)
        self.assertEqual(self.player.rect.height, 90)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.reward, 0)
        self.assertEqual(self.player.active, [True, True])

    def test_update_score(self):
        self.player.update_score(1)
        self.assertEqual(self.player.score, 1)
        self.player.update_score(3)
        self.assertEqual(self.player.score, 4)

    def test_reset(self):
        self.player.rect.x = 200
        self.player.rect.y = 300
        self.player.score = 5
        self.player.active = [False, False]

        self.player.reset()

        self.assertEqual(self.player.rect.x, 25)
        self.assertEqual(self.player.rect.y, 150)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.active, [True, True])

    def test_check_collision(self):
        other = Rectangle(20, 160, 20, 20)
        self.assertTrue(self.player.check_collision(other))

        far = Rectangle(500, 500, 10, 10)
        self.assertFalse(self.player.check_collision(far))


class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(x=350, y=200, width=36, height=36, speedx=4, speedy=5)

    def test_initialization(self):
        self.assertEqual(self.ball.rect.x, 350)
        self.assertEqual(self.ball.rect.y, 200)
        self.assertEqual(self.ball.move_x, 4)
        self.assertEqual(self.ball.move_y, 5)

    def test_normal_movement(self):
        self.ball.move_ball(WIDTH=700, HEIGHT=400)
        self.assertEqual(self.ball.rect.x, 354)
        self.assertEqual(self.ball.rect.y, 205)
        self.assertEqual(self.ball.move_x, 4)
        self.assertEqual(self.ball.move_y, 5)

    def test_bounce_right_wall(self):
        self.ball.rect.x = 680  # >= 700 - 25 = 675
        self.ball.move_ball(WIDTH=700, HEIGHT=400)
        self.assertEqual(self.ball.move_x, -4)

    def test_bounce_left_wall(self):
        self.ball.rect.x = 0
        self.ball.move_x = -4
        self.ball.move_ball(WIDTH=700, HEIGHT=400)
        self.assertEqual(self.ball.move_x, 4)

    def test_bounce_top_wall(self):
        self.ball.rect.y = 0
        self.ball.move_y = -5
        self.ball.move_ball(WIDTH=700, HEIGHT=400)
        self.assertEqual(self.ball.move_y, 5)

    def test_bounce_bottom_wall(self):
        self.ball.rect.y = 380  # >= 400 - 25 = 375
        self.ball.move_ball(WIDTH=700, HEIGHT=400)
        self.assertEqual(self.ball.move_y, -5)

    def test_reset(self):
        self.ball.rect.x = 100
        self.ball.rect.y = 100
        initial_speed_x = self.ball.move_x

        self.ball.reset()

        self.assertEqual(self.ball.rect.x, 350)
        self.assertEqual(self.ball.rect.y, 200)
        self.assertEqual(self.ball.move_x, -initial_speed_x)

    def test_handle_collision_with_player(self):
        player = Player(25, 150, 11, 90, [True])
        player.reward = 0
        initial_speed_x = self.ball.move_x

        self.ball.handle_collision(player, reward=1.5)

        self.assertEqual(self.ball.move_x, -initial_speed_x)
        self.assertEqual(player.reward, 1.5)


if __name__ == "__main__":
    unittest.main()
