import os
import tempfile
import unittest
from unittest.mock import MagicMock
import torch
from tests import conftest

from src.Loaders.AILoader import AILoader, AIModelLoadResult
from src.Type_Model.Neural_Network_Pytorch import SimpleNN_Pytorch
from src.Type_Training.Genetic_Algorithm import save_genetic_model


class TestAILoader(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_config.base_dir = tempfile.mkdtemp()
        self.mock_config.config_AI = {
            "type_training": {"Genetic": True, "Q-learning": False},
            "type_model": {"Pytorch": True, "Tensorflow": False},
            "nn": {"hidden_layers": 2, "neurons_per_layer": 10},
        }
        self.loader = AILoader(self.mock_config)

    def test_selected_training_and_model(self):
        self.assertEqual(self.loader._get_selected_training(), "Genetic")
        self.assertEqual(self.loader._get_selected_model(), "Pytorch")

        # Invalid training
        self.mock_config.config_AI["type_training"] = {"Genetic": False, "Q-learning": False}
        with self.assertRaises(ValueError):
            self.loader._get_selected_training()

        # Invalid model
        self.mock_config.config_AI["type_model"] = {"Pytorch": False, "Tensorflow": False}
        with self.assertRaises(ValueError):
            self.loader._get_selected_model()

    def test_hidden_architecture(self):
        arch = self.loader._get_hidden_architecture()
        self.assertEqual(arch, [10, 10])

    def test_load_model_result_file_not_found(self):
        # AI/best_model.pth does not exist in temporary base_dir
        result = self.loader.load_model_result()
        self.assertIsInstance(result, AIModelLoadResult)
        self.assertFalse(result.model_found)
        self.assertIsNone(result.model)
        self.assertIsNone(result.error_message)

    def test_load_model_result_success(self):
        ai_dir = os.path.join(self.mock_config.base_dir, "AI")
        os.makedirs(ai_dir, exist_ok=True)
        model_path = os.path.join(ai_dir, "best_model.pth")

        # Create and save a valid dummy model
        dummy_model = SimpleNN_Pytorch(input_size=6, output_size=2, hidden_sizes=[10, 10])
        save_genetic_model(dummy_model, optimizer=None, path=model_path)

        result = self.loader.load_model_result()
        self.assertTrue(result.model_found)
        self.assertIsNotNone(result.model)
        self.assertIsNone(result.error_message)


if __name__ == "__main__":
    unittest.main()
