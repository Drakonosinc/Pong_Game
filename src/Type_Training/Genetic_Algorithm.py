import random,copy,torch
from Type_Model import *
def fitness_function(model, game):
    game.model = model  
    score = game.run_with_model()
    return score
