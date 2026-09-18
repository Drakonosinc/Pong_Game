import unittest
import numpy as np
import torch
from tests import conftest

from src.Type_Model.Neural_Network_Pytorch import SimpleNN_Pytorch


class TestNeuralNetworks(unittest.TestCase):
    def test_pytorch_network_forward_and_activations(self):
        # Default hidden layers
        net_default = SimpleNN_Pytorch(input_size=6, output_size=2)
        x_default = torch.randn(1, 6)
        out_default = net_default(x_default)
        self.assertEqual(out_default.shape, (1, 2))
        self.assertIsNotNone(net_default.activations)
        self.assertEqual(net_default.activations.shape, (1, 128))

        # Custom hidden architecture: 3 layers of 16 neurons
        net_custom = SimpleNN_Pytorch(input_size=6, output_size=2, hidden_sizes=[16, 16, 16])
        x_custom = torch.randn(4, 6)  # batch size of 4
        out_custom = net_custom(x_custom)
        self.assertEqual(out_custom.shape, (4, 2))
        self.assertEqual(len(net_custom.hidden_layers), 3)
        self.assertIsNotNone(net_custom.activations)

        # Verify activations are normalized within [0, 1]
        act = net_custom.activations
        self.assertTrue(np.all(act >= 0.0) and np.all(act <= 1.0))

    def test_tensorflow_network_if_installed(self):
        try:
            import tensorflow as tf
            from src.Type_Model.Neural_Network_Tensorflow import SimpleNN_Tensorflow

            net_tf = SimpleNN_Tensorflow(input_size=6, output_size=2, hidden_sizes=[16, 8])
            x_tf = tf.random.normal((1, 6))
            out_tf = net_tf(x_tf)

            self.assertEqual(out_tf.shape, (1, 2))
            self.assertEqual(len(net_tf.hidden_layers), 2)
            self.assertIsNotNone(net_tf.activations)
        except ImportError:
            self.skipTest("TensorFlow no disponible para esta prueba.")


if __name__ == "__main__":
    unittest.main()
