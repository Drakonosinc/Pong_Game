import os
import tempfile
import unittest
from unittest.mock import MagicMock
import numpy as np
import torch
from tests import conftest

from src.Type_Training.Genetic_Algorithm import (
    initialize_population,
    _get_weights_np,
    _set_weights_np,
    select_parents,
    crossover,
    mutate,
    save_genetic_model,
    load_genetic_model,
    genetic_algorithm,
)
from src.Type_Model.Neural_Network_Pytorch import SimpleNN_Pytorch


class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        self.input_size = 6
        self.output_size = 2
        self.hidden_sizes = [8, 8]

    def test_initialize_population(self):
        pop = initialize_population(
            "Pytorch",
            size=5,
            input_size=self.input_size,
            output_size=self.output_size,
            hidden_sizes=self.hidden_sizes,
        )
        self.assertEqual(len(pop), 5)
        for model in pop:
            self.assertIsInstance(model, SimpleNN_Pytorch)

    def test_get_and_set_weights_np(self):
        model = SimpleNN_Pytorch(self.input_size, self.output_size, self.hidden_sizes)
        weights = _get_weights_np(model)

        self.assertIsInstance(weights, list)
        self.assertGreater(len(weights), 0)

        # Alter weights manually and set them
        modified_weights = [w * 0.0 + 1.23 for w in weights]
        _set_weights_np(model, modified_weights)

        retrieved = _get_weights_np(model)
        for r in retrieved:
            np.testing.assert_allclose(r, 1.23, rtol=1e-5)

    def test_select_parents(self):
        pop = initialize_population("Pytorch", 4, self.input_size, self.output_size, self.hidden_sizes)
        fitness_scores = [10.0, 50.0, 100.0, 20.0]

        parents = select_parents(pop, fitness_scores, num_parents=2)
        self.assertEqual(len(parents), 2)
        for p in parents:
            self.assertIn(p, pop)

    def test_crossover(self):
        p1 = SimpleNN_Pytorch(self.input_size, self.output_size, self.hidden_sizes)
        p2 = SimpleNN_Pytorch(self.input_size, self.output_size, self.hidden_sizes)

        # Make weights distinctly different
        w1 = [np.ones_like(w) * 10.0 for w in _get_weights_np(p1)]
        w2 = [np.ones_like(w) * 20.0 for w in _get_weights_np(p2)]
        _set_weights_np(p1, w1)
        _set_weights_np(p2, w2)

        c1, c2 = crossover(p1, p2, "Pytorch", self.input_size, self.output_size, self.hidden_sizes)

        c1_w = _get_weights_np(c1)
        c2_w = _get_weights_np(c2)

        for w in c1_w:
            # Every weight value should be either 10.0 or 20.0
            self.assertTrue(np.all((w == 10.0) | (w == 20.0)))
        for w in c2_w:
            self.assertTrue(np.all((w == 10.0) | (w == 20.0)))

    def test_mutate(self):
        model = SimpleNN_Pytorch(self.input_size, self.output_size, self.hidden_sizes)
        original_weights = [w.copy() for w in _get_weights_np(model)]

        # 100% mutation rate guarantees changes
        mutate(model, mutation_rate=1.0, mutation_strength=0.5)
        mutated_weights = _get_weights_np(model)

        for orig, mut in zip(original_weights, mutated_weights):
            self.assertFalse(np.array_equal(orig, mut))

    def test_save_and_load_genetic_model(self):
        model = SimpleNN_Pytorch(self.input_size, self.output_size, self.hidden_sizes)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "best_model.pth")
            save_genetic_model(model, optimizer=None, path=path)
            self.assertTrue(os.path.exists(path))

            loaded = load_genetic_model(
                path,
                "Pytorch",
                self.input_size,
                self.output_size,
                hidden_sizes=self.hidden_sizes,
            )
            self.assertIsNotNone(loaded)

            orig_w = _get_weights_np(model)
            loaded_w = _get_weights_np(loaded)
            for ow, lw in zip(orig_w, loaded_w):
                np.testing.assert_allclose(ow, lw, rtol=1e-5)

    def test_genetic_algorithm_run(self):
        mock_game = MagicMock()
        mock_game.exit = False
        # Mock fitness reward
        mock_game.run_with_model.return_value = 15.0

        best = genetic_algorithm(
            game=mock_game,
            type_model="Pytorch",
            input_size=self.input_size,
            output_size=self.output_size,
            generations=1,
            population_size=4,
            num_trials=1,
            hidden_sizes=self.hidden_sizes,
        )
        self.assertIsNotNone(best)
        self.assertIs(mock_game.model, best)


if __name__ == "__main__":
    unittest.main()
