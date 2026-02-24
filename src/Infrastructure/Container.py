import sys
from src.Infrastructure.AI.Adapters.PyTorchAdapter import PyTorchAdapter
from src.Infrastructure.AI.Adapters.MockAdapter import MockAdapter
from src.Infrastructure.Training.TrainingAdapters import GeneticTrainer, QLearningTrainer
from src.Game.Space_Pong import Space_pong_game
class Container:
    def __init__(self):
