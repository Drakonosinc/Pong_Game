import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import copy
from collections import deque
from Type_Model import *
class ReplayMemory:
    def __init__(self, capacity: int): self.memory = deque(maxlen=capacity)
    def push(self, transition: tuple): self.memory.append(transition)
    def sample(self, batch_size: int): return random.sample(self.memory, batch_size)
    def __len__(self) -> int: return len(self.memory)
class DQNAgent:
    def __init__(self, type_model, state_size: int, action_size: int, lr: float = 1e-3, gamma: float = 0.99, 
                epsilon_start: float = 1.0, epsilon_end: float = 0.01, epsilon_decay: float = 0.995, 
                memory_size: int = 10000, batch_size: int = 32, target_update: int = 100, hidden_sizes=None):
        self.state_size = state_size
        self.action_size = action_size
        self._hidden_sizes = hidden_sizes
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.steps_done = 0
        self.target_update = target_update
        if type_model == "Pytorch":
            self.policy_net = SimpleNN_Pytorch(state_size, action_size, hidden_sizes=self._hidden_sizes)
            self.target_net = SimpleNN_Pytorch(state_size, action_size, hidden_sizes=self._hidden_sizes)
        elif type_model == "Tensorflow":
            self.policy_net = SimpleNN_Tensorflow(state_size, action_size, hidden_sizes=self._hidden_sizes)
            self.target_net = SimpleNN_Tensorflow(state_size, action_size, hidden_sizes=self._hidden_sizes)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(memory_size)
    def select_action(self, state: np.ndarray) -> int:
        if random.random() < self.epsilon: return random.randrange(self.action_size)
        with torch.no_grad():
            tensor_state = torch.tensor(state, dtype=torch.float32)
            q_values = self.policy_net(tensor_state)
            return int(torch.argmax(q_values).item())
    def store_transition(self, state, action, reward, next_state, done): self.memory.push((state, action, reward, next_state, done))
    def optimize_model(self):
        if len(self.memory) < self.batch_size: return
        transitions = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*transitions)
        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)
        current_q = self.policy_net(states).gather(1, actions)
        next_q = self.target_net(next_states).max(1)[0].detach().unsqueeze(1)
        expected_q = rewards + (1 - dones) * self.gamma * next_q
        loss = nn.MSELoss()(current_q, expected_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.steps_done += 1
        if self.steps_done % self.target_update == 0: self.target_net.load_state_dict(self.policy_net.state_dict())
class QLearningTrainer:
    def __init__(self, game, type_model, input_size, output_size, episodes=500, lr=1e-3, 
                gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, hidden_sizes=None):
        self.game = game
        self.episodes = episodes
        self.current_episode = 0
        self.best_reward = float('-inf')
        self.best_model = None
        self.rewards_history = []
        self.agent = DQNAgent(type_model=type_model,
                            state_size=input_size, 
                            action_size=output_size,
                            lr=lr, gamma=gamma,
                            epsilon_start=epsilon_start,
                            epsilon_end=epsilon_end,
                            epsilon_decay=epsilon_decay,
                            hidden_sizes=hidden_sizes)
        print(f"Q-Learning trainer initialized for {episodes} episodes")
    def get_action(self, state): return self.agent.select_action(state)
    def store_experience(self, state, action, reward, next_state, done):
        self.agent.store_transition(state, action, reward, next_state, done)
        self.agent.optimize_model()
    def episode_complete(self, total_reward):
        self.rewards_history.append(total_reward)
        if total_reward > self.best_reward:
            self.best_reward = total_reward
            self.best_model = copy.deepcopy(self.agent.policy_net)
        if self.current_episode % 10 == 0:
            avg_reward = np.mean(self.rewards_history[-10:]) if len(self.rewards_history) >= 10 else np.mean(self.rewards_history)
            print(f"Episode {self.current_episode}/{self.episodes}: Avg Reward = {avg_reward:.2f}, Epsilon = {self.agent.epsilon:.3f}")
        self.current_episode += 1
        if self.current_episode >= self.episodes:
            print(f"Q-Learning training completed. Best reward: {self.best_reward:.2f}")
            return True
        return False
    def get_best_model(self): return self.best_model if self.best_model is not None else self.agent.policy_net
_qlearning_trainer = None
def q_learning_step(game, state, action):
    global _qlearning_trainer
    if _qlearning_trainer is None: return
    if action == 0 and game.player_two.rect.top > 0: game.player_two.rect.y -= 5 # UP
    elif action == 1 and game.player_two.rect.bottom < game.HEIGHT: game.player_two.rect.y += 5 # DOWN
def q_learning_algorithm(game, type_model, input_size, output_size, episodes=500, lr=1e-3, 
                        gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, hidden_sizes=None):
    global _qlearning_trainer
    _qlearning_trainer = QLearningTrainer(game, type_model, input_size, output_size, episodes, lr, gamma, epsilon_start, epsilon_end, epsilon_decay, hidden_sizes=hidden_sizes)
    game._qlearning_state = None
    game._qlearning_prev_reward = 0
    while _qlearning_trainer.current_episode < episodes:
        game.generation = _qlearning_trainer.current_episode
        total_reward = game.run_with_model()
        training_complete = _qlearning_trainer.episode_complete(total_reward)
        if training_complete or game.exit: break
    best_model = _qlearning_trainer.get_best_model()
    if hasattr(game, '_qlearning_state'): delattr(game, '_qlearning_state')
    if hasattr(game, '_qlearning_prev_reward'): delattr(game, '_qlearning_prev_reward')
    _qlearning_trainer = None
    game.model = best_model
    return best_model
def save_qlearning_model(model, optimizer, path):
    """Save Q-learning model (same interface as genetic algorithm)"""
    print("Saving Q-learning model")
    torch.save({'model_state_dict': model.state_dict(),'optimizer_state_dict': optimizer.state_dict(),}, path)
def load_qlearning_model(path, model, optimizer=None):
    """Load Q-learning model (same interface as genetic algorithm)"""
    try:
        print("Loading Q-learning model")
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer: optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None