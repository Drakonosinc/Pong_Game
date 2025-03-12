import torch
import numpy as np
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.model
    def get_state(self):
        return np.array([self.player_one.rect.x, self.player_one.rect.y, self.player_two.rect.x, self.player_two.rect.y,self.balls[0].rect.x,self.balls[0].rect.y])
    def action_ai(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.IA_actions(action)
    