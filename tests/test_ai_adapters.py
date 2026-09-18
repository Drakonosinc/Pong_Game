import os
import tempfile
import unittest
from unittest.mock import MagicMock
import numpy as np
import torch
import torch.nn as nn
from tests import conftest

from src.Infrastructure.AI.Adapters.MockAdapter import MockAdapter
from src.Infrastructure.AI.Adapters.PyTorchAdapter import PyTorchAdapter
from src.AI.AI_Controller import AIHandler
from src.Events.EventManager import EventManager
from src.Events.GameEvents import GameStateChangedEvent, ActionDecidedEvent
from src.Core.Domain.DTOs import WorldStateDTO


class DummyTorchModel(nn.Module):
    def __init__(self, in_features=6, out_features=2):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x):
        return self.linear(x)


class TestAIAdapters(unittest.TestCase):
    def test_mock_adapter_predict(self):
        adapter = MockAdapter(output_size=3)
        dummy_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        prediction = adapter.predict(dummy_state)

        self.assertIsInstance(prediction, np.ndarray)
        self.assertEqual(prediction.shape, (3,))
        self.assertTrue(np.all(prediction >= -1.0) and np.all(prediction <= 1.0))
        self.assertIsNone(adapter.get_internal_model())

    def test_pytorch_adapter_predict_and_persistence(self):
        torch_model = DummyTorchModel()
        adapter = PyTorchAdapter(torch_model)

        state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=np.float32)
        prediction = adapter.predict(state)

        self.assertIsInstance(prediction, np.ndarray)
        self.assertEqual(prediction.shape, (2,))
        self.assertIs(adapter.get_internal_model(), torch_model)

        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = os.path.join(temp_dir, "test_torch.pth")
            adapter.save(save_path)
            self.assertTrue(os.path.exists(save_path))

            fresh_model = DummyTorchModel()
            fresh_adapter = PyTorchAdapter(fresh_model)
            fresh_adapter.load(save_path)

            pred_after_load = fresh_adapter.predict(state)
            np.testing.assert_allclose(prediction, pred_after_load, rtol=1e-5)

    def test_tensorflow_adapter_if_installed(self):
        try:
            import tensorflow as tf
            from src.Infrastructure.AI.Adapters.TensorFlowAdapter import TensorFlowAdapter

            inputs = tf.keras.Input(shape=(6,))
            outputs = tf.keras.layers.Dense(2)(inputs)
            tf_model = tf.keras.Model(inputs=inputs, outputs=outputs)

            adapter = TensorFlowAdapter(tf_model)
            state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=np.float32)
            prediction = adapter.predict(state)

            self.assertIsInstance(prediction, np.ndarray)
            self.assertEqual(prediction.shape, (2,))
            self.assertIs(adapter.get_internal_model(), tf_model)
        except ImportError:
            self.skipTest("TensorFlow no disponible para esta prueba.")


class TestAIHandler(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.em = EventManager()
        self.game.event_manager = self.em
        self.game.config.config_AI = {
            "type_training": {"Genetic": True, "Q-learning": False},
            "type_model": {"Pytorch": True, "Tensorflow": False},
        }
        self.handler = AIHandler(self.game)

    def test_get_state_from_game_logic(self):
        mock_logic = MagicMock()
        mock_logic.player_one.rect.x = 25.0
        mock_logic.player_one.rect.y = 150.0
        mock_logic.player_two.rect.x = 665.0
        mock_logic.player_two.rect.y = 160.0
        mock_logic.balls = [MagicMock(rect=MagicMock(x=350.0, y=200.0))]
        self.game.game_logic = mock_logic

        state = self.handler.get_state()
        self.assertEqual(state.shape, (6,))
        np.testing.assert_array_equal(state, [25.0, 150.0, 665.0, 160.0, 350.0, 200.0])

    def test_handle_game_state_changed_with_adapter(self):
        mock_adapter = MagicMock()
        mock_adapter.predict.return_value = np.array([1.0, -1.0])
        self.handler.set_model(mock_adapter)

        posted_events = []
        self.em.subscribe(ActionDecidedEvent, lambda ev: posted_events.append(ev))

        dto = WorldStateDTO(25, 150, 665, 150, 350, 200)
        self.em.post(GameStateChangedEvent(dto, player_two_reward=0, p1_score=0, p2_score=0))

        self.assertEqual(len(posted_events), 1)
        np.testing.assert_array_equal(posted_events[0].action, [1.0, -1.0])

    def test_set_runtime_model_wrapping(self):
        torch_model = DummyTorchModel()
        self.handler.set_runtime_model(torch_model)
        self.assertIsInstance(self.handler.model_adapter, PyTorchAdapter)
        self.assertIs(self.handler.model_adapter.get_internal_model(), torch_model)

        self.handler.clear_model()
        self.assertIsNone(self.handler.model_adapter)

    def test_reset_qlearning_state(self):
        self.handler.prev_state = np.zeros(6)
        self.handler.prev_action = 1
        self.handler.prev_reward = 10.0

        self.handler.reset_qlearning_state()

        self.assertIsNone(self.handler.prev_state)
        self.assertIsNone(self.handler.prev_action)
        self.assertEqual(self.handler.prev_reward, 0)


if __name__ == "__main__":
    unittest.main()
