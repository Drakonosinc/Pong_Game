import os
import json
import tempfile
import unittest
from tests import conftest

from src.Loaders.Config_Loader import Config


class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.config(alls=True)

    def test_default_config_generation(self):
        self.assertIn("WIDTH", self.config.config_visuals)
        self.assertEqual(self.config.config_visuals["WIDTH"], 700)
        self.assertEqual(self.config.config_visuals["HEIGHT"], 400)

        self.assertIn("UP_W", self.config.config_keys)
        self.assertIn("sound_main", self.config.config_sounds)
        self.assertIn("genetic", self.config.config_AI)
        self.assertIn("q_learning", self.config.config_AI)
        self.assertIn("number_balls", self.config.config_game)

    def test_deep_update(self):
        target = {"a": 1, "nested": {"x": 10, "y": 20}}
        source = {"nested": {"y": 99, "z": 30}, "b": 2}
        result = self.config._deep_update(target, source)

        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)
        self.assertEqual(result["nested"]["x"], 10)
        self.assertEqual(result["nested"]["y"], 99)
        self.assertEqual(result["nested"]["z"], 30)

    def test_validate_and_normalize_clamps_invalid_values(self):
        # Set negative or corrupted values
        self.config.config_visuals["WIDTH"] = -100
        self.config.config_visuals["HEIGHT"] = 0
        self.config.config_visuals["value_background"] = 999  # Out of range index
        self.config.config_game["number_balls"] = -5
        self.config.config_game["max_score"] = 0
        self.config.config_AI["genetic"]["generation_value"] = -1
        self.config.config_AI["q_learning"]["episodes"] = 0
        self.config.config_AI["nn"]["hidden_layers"] = -3
        self.config.config_AI["type_training"] = {"Genetic": False, "Q-learning": False}
        self.config.config_AI["type_model"] = {"Pytorch": False, "Tensorflow": False}

        self.config._validate_and_normalize()

        self.assertGreaterEqual(self.config.config_visuals["WIDTH"], 1)
        self.assertGreaterEqual(self.config.config_visuals["HEIGHT"], 1)
        self.assertLess(
            self.config.config_visuals["value_background"],
            len(self.config.config_visuals["image_background"]),
        )
        self.assertGreaterEqual(self.config.config_game["number_balls"], 1)
        self.assertGreaterEqual(self.config.config_game["max_score"], 1)
        self.assertGreaterEqual(self.config.config_AI["genetic"]["generation_value"], 1)
        self.assertGreaterEqual(self.config.config_AI["q_learning"]["episodes"], 1)
        self.assertGreaterEqual(self.config.config_AI["nn"]["hidden_layers"], 1)
        self.assertTrue(self.config.config_AI["type_training"]["Genetic"])
        self.assertTrue(self.config.config_AI["type_model"]["Pytorch"])

    def test_save_and_load_in_isolated_temp_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_config = Config()
            test_config.base_dir = temp_dir
            test_config.config_dir = os.path.join(temp_dir, "Config")
            test_config.config(alls=True)

            # Modify specific fields
            test_config.config_visuals["WIDTH"] = 1024
            test_config.config_visuals["HEIGHT"] = 768
            test_config.config_game["number_balls"] = 3
            test_config.config_sounds["sound_main"] = False

            # Save to temporary config directory
            test_config.save_config()

            # Verify files were generated
            for name in ("visuals.json", "keybindings.json", "settings.json", "ai_config.json"):
                self.assertTrue(os.path.exists(os.path.join(test_config.config_dir, name)))

            # Now create a fresh config and load from the temp directory
            loader_config = Config()
            loader_config.base_dir = temp_dir
            loader_config.config_dir = os.path.join(temp_dir, "Config")
            loader_config.load_config()

            self.assertEqual(loader_config.config_visuals["WIDTH"], 1024)
            self.assertEqual(loader_config.config_visuals["HEIGHT"], 768)
            self.assertEqual(loader_config.config_game["number_balls"], 3)
            self.assertFalse(loader_config.config_sounds["sound_main"])

    def test_load_visuals_formats(self):
        # Format 1: Direct config_visuals wrapper
        data1 = {"config_visuals": {"WIDTH": 800, "HEIGHT": 600}}
        self.config._load_visuals(data1)
        self.assertEqual(self.config.config_visuals["WIDTH"], 800)

        # Format 2: Window and assets split
        data2 = {
            "window": {"width": 1280, "height": 720},
            "assets": {"value_background": 1, "value_planet": 2},
        }
        self.config._load_visuals(data2)
        self.assertEqual(self.config.config_visuals["WIDTH"], 1280)
        self.assertEqual(self.config.config_visuals["HEIGHT"], 720)
        self.assertEqual(self.config.config_visuals["value_background"], 1)
        self.assertEqual(self.config.config_visuals["value_planet"], 2)


if __name__ == "__main__":
    unittest.main()
