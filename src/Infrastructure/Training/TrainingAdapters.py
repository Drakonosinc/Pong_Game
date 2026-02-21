import torch
from src.Core.Interfaces.ITrainer import ITrainer
from src.Type_Training.Genetic_Algorithm import genetic_algorithm, save_genetic_model
from src.Type_Training.Q_learning import q_learning_algorithm, save_qlearning_model
class GeneticTrainer(ITrainer):
