import torch
import numpy as np
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.model
    def get_state(self):
        return np.array([self.game.player_one.rect.x, self.game.player_one.rect.y, self.game.player_two.rect.x, 
                        self.game.player_two.rect.y,self.game.balls[0].rect.x,self.game.balls[0].rect.y])
    def action_ai(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)
    def AI_actions(self,action):
        if action[0]>0 and self.game.player_two.rect.top > 0:self.game.player_two.rect.y -= 5
        if action[0]<0 and self.game.player_two.rect.bottom < self.game.HEIGHT:self.game.player_two.rect.y += 5