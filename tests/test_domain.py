import unittest
import numpy as np
from tests import conftest  # Configura sys.path y variables dummy

from src.Core.Domain.Geometry import Rectangle
from src.Core.Domain.DTOs import WorldStateDTO
from src.Core.GameContext import GameContext
from src.Core.Interfaces.IAIModel import IAIModel
from src.Core.Interfaces.ISoundService import IAudioService
from src.Core.Interfaces.ITrainer import ITrainer


class TestRectangle(unittest.TestCase):
    def setUp(self):
        self.rect = Rectangle(10.0, 20.0, 30.0, 40.0)

    def test_properties(self):
        self.assertEqual(self.rect.left, 10.0)
        self.assertEqual(self.rect.top, 20.0)
        self.assertEqual(self.rect.right, 40.0)
        self.assertEqual(self.rect.bottom, 60.0)
        self.assertEqual(self.rect.center, (25.0, 40.0))

    def test_to_tuple_and_indexing(self):
        self.assertEqual(self.rect.to_tuple(), (10.0, 20.0, 30.0, 40.0))
        self.assertEqual(len(self.rect), 4)
        self.assertEqual(self.rect[0], 10.0)
        self.assertEqual(self.rect[1], 20.0)
        self.assertEqual(self.rect[2], 30.0)
        self.assertEqual(self.rect[3], 40.0)
        self.assertEqual(list(self.rect), [10.0, 20.0, 30.0, 40.0])

    def test_collision_detection(self):
        overlapping = Rectangle(20.0, 30.0, 30.0, 30.0)
        self.assertTrue(self.rect.colliderect(overlapping))
        self.assertTrue(overlapping.colliderect(self.rect))

        non_overlapping = Rectangle(100.0, 100.0, 20.0, 20.0)
        self.assertFalse(self.rect.colliderect(non_overlapping))

        # Adjacent rectangles (touching borders but not overlapping)
        adjacent = Rectangle(40.0, 20.0, 30.0, 40.0)
        self.assertFalse(self.rect.colliderect(adjacent))

        # Invalid type comparison
        self.assertFalse(self.rect.colliderect("not_a_rect"))
        self.assertFalse(self.rect.colliderect(None))


class TestWorldStateDTO(unittest.TestCase):
    def test_dto_values_and_array_conversion(self):
        dto = WorldStateDTO(p1_x=25.0, p1_y=150.0, p2_x=665.0, p2_y=150.0, ball_x=322.0, ball_y=171.0)
        arr = dto.to_array()

        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (6,))
        self.assertEqual(arr.dtype, np.float32)
        np.testing.assert_allclose(arr, [25.0, 150.0, 665.0, 150.0, 322.0, 171.0])

    def test_frozen_immutability(self):
        dto = WorldStateDTO(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        with self.assertRaises(Exception):
            dto.p1_x = 100.0


class TestGameContext(unittest.TestCase):
    def test_context_references(self):
        mock_config = object()
        mock_assets = object()
        mock_events = object()
        mock_window = object()

        context = GameContext(mock_config, mock_assets, mock_events, mock_window)
        self.assertIs(context.config, mock_config)
        self.assertIs(context.assets, mock_assets)
        self.assertIs(context.event_manager, mock_events)
        self.assertIs(context.window_manager, mock_window)
        self.assertIs(context.sound, mock_assets)


class TestInterfaces(unittest.TestCase):
    def test_abstract_interfaces_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            IAIModel()
        with self.assertRaises(TypeError):
            IAudioService()
        with self.assertRaises(TypeError):
            ITrainer()


if __name__ == "__main__":
    unittest.main()
