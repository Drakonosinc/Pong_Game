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
        self.AI_actions(action)
    def AI_actions(self,action):
        if action[0]>0 and self.player_two.rect.top > 0:self.player_two.rect.y -= 5
        if action[0]<0 and self.player_two.rect.bottom < self.HEIGHT:self.player_two.rect.y += 5