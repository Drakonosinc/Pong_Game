import numpy as np
try: import tensorflow as tf
except ImportError: tf = None
from src.Core.Interfaces.IAIModel import IAIModel
class TensorFlowAdapter(IAIModel):
