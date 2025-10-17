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
    def __len__(self) -> int:
        return len(self.memory)

class DQNAgent:
    def __init__(self, state_size: int, action_size: int, lr: float = 1e-3, gamma: float = 0.99, 
                 epsilon_start: float = 1.0, epsilon_end: float = 0.01, epsilon_decay: float = 0.995, 
                 memory_size: int = 10000, batch_size: int = 32, target_update: int = 100):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.steps_done = 0
        self.target_update = target_update
        
        # Create networks - use SimpleNN for consistency with genetic algorithm
        self.policy_net = SimpleNN(state_size, action_size)
        self.target_net = SimpleNN(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(memory_size)
        
    def select_action(self, state: np.ndarray) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        with torch.no_grad():
            tensor_state = torch.tensor(state, dtype=torch.float32)
            q_values = self.policy_net(tensor_state)
            return int(torch.argmax(q_values).item())
            
    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push((state, action, reward, next_state, done))
        
    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return
            
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
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.steps_done += 1
        
        # Update target network
        if self.steps_done % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

class QLearningTrainer:
    """Q-learning trainer that integrates with the existing game architecture"""
    def __init__(self, game, input_size, output_size, episodes=500, lr=1e-3, 
                 gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
        self.game = game
        self.episodes = episodes
        self.current_episode = 0
        self.best_reward = float('-inf')
        self.best_model = None
        self.rewards_history = []
        
        # Create DQN agent
        self.agent = DQNAgent(
            state_size=input_size, 
            action_size=output_size, 
            lr=lr, 
            gamma=gamma,
            epsilon_start=epsilon_start, 
            epsilon_end=epsilon_end, 
            epsilon_decay=epsilon_decay
        )
        
        print(f"Q-Learning trainer initialized for {episodes} episodes")
    
    def get_action(self, state):
        """Get action from Q-learning agent"""
        return self.agent.select_action(state)
    
    def store_experience(self, state, action, reward, next_state, done):
        """Store experience and optimize model"""
        self.agent.store_transition(state, action, reward, next_state, done)
        self.agent.optimize_model()
    
    def episode_complete(self, total_reward):
        """Called when an episode is complete"""
        self.rewards_history.append(total_reward)
        
        # Track best model
        if total_reward > self.best_reward:
            self.best_reward = total_reward
            self.best_model = copy.deepcopy(self.agent.policy_net)
        
        # Print progress
        if self.current_episode % 10 == 0:
            avg_reward = np.mean(self.rewards_history[-10:]) if len(self.rewards_history) >= 10 else np.mean(self.rewards_history)
            print(f"Episode {self.current_episode}/{self.episodes}: Avg Reward = {avg_reward:.2f}, Epsilon = {self.agent.epsilon:.3f}")
        
        self.current_episode += 1
        
        # Check if training is complete
        if self.current_episode >= self.episodes:
            print(f"Q-Learning training completed. Best reward: {self.best_reward:.2f}")
            return True
        
        return False
    
    def get_best_model(self):
        """Get the best model found during training"""
        return self.best_model if self.best_model is not None else self.agent.policy_net

# Global trainer instance
_qlearning_trainer = None

def q_learning_step(game, state, action):
    """Execute one step of Q-learning training"""
    global _qlearning_trainer
    if _qlearning_trainer is None:
        return
    
    # Apply Q-learning action to player_two
    if action == 0 and game.player_two.rect.top > 0:  # UP
        game.player_two.rect.y -= 5
    elif action == 1 and game.player_two.rect.bottom < game.HEIGHT:  # DOWN
        game.player_two.rect.y += 5

def q_learning_algorithm(game, input_size, output_size, episodes=500, lr=1e-3, 
                        gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
    """Main Q-learning training function that integrates with the game like genetic algorithm"""
    global _qlearning_trainer
    
    # Create trainer instance
    _qlearning_trainer = QLearningTrainer(
        game, input_size, output_size, episodes, lr, gamma, epsilon_start, epsilon_end, epsilon_decay
    )
    
    # Initialize Q-learning state tracking
    game._qlearning_state = None
    game._qlearning_prev_reward = 0
    
    # Run training episodes using the existing run_with_model structure
    while _qlearning_trainer.current_episode < episodes:
        game.generation = _qlearning_trainer.current_episode
        
        # Run one episode using the existing game loop
        total_reward = game.run_with_model()
        
        # Episode complete
        training_complete = _qlearning_trainer.episode_complete(total_reward)
        
        if training_complete or game.exit:
            break
    
    # Get best model
    best_model = _qlearning_trainer.get_best_model()
    
    # Cleanup
    if hasattr(game, '_qlearning_state'):
        delattr(game, '_qlearning_state')
    if hasattr(game, '_qlearning_prev_reward'):
        delattr(game, '_qlearning_prev_reward')
    
    _qlearning_trainer = None
    
    # Set the best model to the game
    game.model = best_model
    return best_model

def save_qlearning_model(model, optimizer, path):
    """Save Q-learning model (same interface as genetic algorithm)"""
    print("Saving Q-learning model")
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)

def load_qlearning_model(path, input_size, output_size, optimizer=None):
    """Load Q-learning model (same interface as genetic algorithm)"""
    try:
        print("Loading Q-learning model")
        model = SimpleNN(input_size, output_size)
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None