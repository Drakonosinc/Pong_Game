import os
import tempfile
import unittest
from unittest.mock import MagicMock
import numpy as np
import torch
from tests import conftest

from src.Type_Training.Q_learning import (
    ReplayMemory,
    DQNAgent,
    QLearningTrainer,
    save_qlearning_model,
    load_qlearning_model,
)


class TestQLearning(unittest.TestCase):
    def test_replay_memory(self):
        mem = ReplayMemory(capacity=3)
        self.assertEqual(len(mem), 0)

        mem.push((1, 0, 1.0, 2, False))
        mem.push((2, 1, 0.5, 3, False))
        mem.push((3, 0, -1.0, 4, True))
        self.assertEqual(len(mem), 3)

        # Adding fourth element should drop the oldest due to maxlen=3
        mem.push((4, 1, 2.0, 5, False))
        self.assertEqual(len(mem), 3)

        sample = mem.sample(batch_size=2)
        self.assertEqual(len(sample), 2)
        for s in sample:
            self.assertEqual(len(s), 5)

    def test_dqn_agent_initialization_and_action_selection(self):
        agent = DQNAgent(
            type_model="Pytorch",
            state_size=6,
            action_size=2,
            epsilon_start=0.0,  # Pure exploitation for deterministic test
            hidden_sizes=[8, 8],
        )
        dummy_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=np.float32)
        action = agent.select_action(dummy_state)
        self.assertIn(action, [0, 1])

        # Test exploration (epsilon = 1.0)
        agent.epsilon = 1.0
        actions = [agent.select_action(dummy_state) for _ in range(20)]
        self.assertTrue(all(a in [0, 1] for a in actions))

    def test_dqn_agent_optimize_step(self):
        agent = DQNAgent(
            type_model="Pytorch",
            state_size=6,
            action_size=2,
            batch_size=4,
            memory_size=100,
            hidden_sizes=[8],
        )

        # Not enough transitions yet
        agent.optimize_model()
        self.assertEqual(agent.steps_done, 0)

        # Fill memory with >= batch_size transitions
        for _ in range(5):
            s = np.random.randn(6).astype(np.float32)
            s_next = np.random.randn(6).astype(np.float32)
            agent.store_transition(s, 0, 1.0, s_next, False)

        initial_eps = agent.epsilon
        agent.optimize_model()

        self.assertEqual(agent.steps_done, 1)
        self.assertLess(agent.epsilon, initial_eps)

    def test_qlearning_trainer_lifecycle(self):
        mock_game = MagicMock()
        trainer = QLearningTrainer(
            game=mock_game,
            type_model="Pytorch",
            input_size=6,
            output_size=2,
            episodes=2,
            hidden_sizes=[8],
        )

        action = trainer.get_action(np.zeros(6, dtype=np.float32))
        self.assertIn(action, [0, 1])

        trainer.store_experience(
            state=np.zeros(6),
            action=action,
            reward=1.0,
            next_state=np.zeros(6),
            done=False,
        )

        # Episode 1 complete (best reward updated)
        done = trainer.episode_complete(total_reward=10.0)
        self.assertFalse(done)
        self.assertEqual(trainer.best_reward, 10.0)

        # Episode 2 complete (reaches limit of 2)
        done = trainer.episode_complete(total_reward=5.0)
        self.assertTrue(done)
        self.assertEqual(trainer.best_reward, 10.0)

        best_net = trainer.get_best_model()
        self.assertIsNotNone(best_net)

    def test_save_and_load_qlearning_model(self):
        agent = DQNAgent(
            type_model="Pytorch",
            state_size=6,
            action_size=2,
            hidden_sizes=[8, 8],
        )
        model = agent.policy_net

        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "q_model.pth")
            save_qlearning_model(model, agent.optimizer, path)
            self.assertTrue(os.path.exists(path))

            loaded = load_qlearning_model(
                path,
                model_or_type_model="Pytorch",
                input_size=6,
                output_size=2,
                hidden_sizes=[8, 8],
            )
            self.assertIsNotNone(loaded)

            # Compare weights
            for p1, p2 in zip(model.parameters(), loaded.parameters()):
                np.testing.assert_allclose(p1.detach().cpu().numpy(), p2.detach().cpu().numpy())


if __name__ == "__main__":
    unittest.main()
