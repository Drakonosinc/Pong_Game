import unittest
from unittest.mock import MagicMock
from tests import conftest

from src.Infrastructure.Container import Container
from src.Infrastructure.Training.TrainingAdapters import GeneticTrainer, QLearningTrainer
from src.Train_Headless import HeadlessEnvironment, MockAudioService


class TestContainerAndHeadless(unittest.TestCase):
    def test_container_trainer_resolution(self):
        container = Container()

        # Uninitialized container raises RuntimeError
        with self.assertRaises(RuntimeError):
            container.get_trainer()

        mock_game = MagicMock()
        container.game = mock_game

        # Test Genetic strategy resolution
        mock_game.config.config_AI = {"type_training": {"Genetic": True, "Q-learning": False}}
        trainer_genetic = container.get_trainer()
        self.assertIsInstance(trainer_genetic, GeneticTrainer)

        # Test Q-learning strategy resolution
        mock_game.config.config_AI = {"type_training": {"Genetic": False, "Q-learning": True}}
        trainer_ql = container.get_trainer()
        self.assertIsInstance(trainer_ql, QLearningTrainer)

        # Test invalid configuration raises ValueError
        mock_game.config.config_AI = {"type_training": {"Genetic": False, "Q-learning": False}}
        with self.assertRaises(ValueError):
            container.get_trainer()

    def test_headless_environment_lifecycle(self):
        env = HeadlessEnvironment()
        self.assertEqual(env.WIDTH, env.config.config_visuals["WIDTH"])
        self.assertEqual(env.HEIGHT, env.config.config_visuals["HEIGHT"])
        self.assertIsInstance(env.audio_service, MockAudioService)
        self.assertTrue(env.mode_game["Training AI"])

        # Test reset
        env.player_one.score = 2
        env.reset(running=True)
        self.assertEqual(env.player_one.score, 0)
        self.assertTrue(env.running)

        # Simulate game loop until score reaches max_score
        env.config.config_game["max_score"] = 1
        env.player_two.score = 1
        env.run()
        self.assertFalse(env.running)


if __name__ == "__main__":
    unittest.main()
