import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import copy
from collections import deque
from Type_Model import *

class ReplayMemory:
    def __init__(self, capacity: int):
        self.memory = deque(maxlen=capacity)
    def push(self, transition: tuple):
        self.memory.append(transition)
    def sample(self, batch_size: int):
        return random.sample(self.memory, batch_size)
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

def q_learning_episode(game, model, agent):
    """Run a single episode for Q-learning training"""
    game.reset(running=True)
    game.player_two.reward = 0
    
    state = game.ai_handler.get_state()
    total_reward = 0
    steps = 0
    max_steps = 1000  # Prevent infinite episodes
    
    while steps < max_steps:
        # Select action using epsilon-greedy
        action = agent.select_action(state)
        
        # Convert action to game movement
        if action == 0:  # UP
            if game.player_two.rect.top > 0:
                game.player_two.rect.y -= 5
        elif action == 1:  # DOWN
            if game.player_two.rect.bottom < game.HEIGHT:
                game.player_two.rect.y += 5
        
        # Simple AI for player one (follows ball)
        if game.player_one.rect.top > 0 or game.player_one.rect.bottom < game.HEIGHT:
            game.player_one.rect.y += game.balls[0].move_y
        if game.player_one.rect.y >= 310:
            game.player_one.rect.y = 310
        if game.player_one.rect.y <= 0:
            game.player_one.rect.y = 0
        
        # Update game state
        game.update()
        
        # Get next state and reward
        next_state = game.ai_handler.get_state()
        reward = game.player_two.reward - total_reward
        total_reward = game.player_two.reward
        
        # Check if episode is done
        done = (game.player_one.score >= game.config.config_game["max_score"] or 
                game.player_two.score >= game.config.config_game["max_score"])
        
        # Store transition
        agent.store_transition(state, action, reward, next_state, done)
        
        # Optimize model
        agent.optimize_model()
        
        state = next_state
        steps += 1
        
        if done:
            break
    
    return total_reward

def q_learning_algorithm(game, input_size, output_size, episodes=500, lr=1e-3, 
                        gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
    """Main Q-learning training function that integrates with the game like genetic algorithm"""
    print(f"Starting Q-Learning training with {episodes} episodes...")
    
    # Create DQN agent
    agent = DQNAgent(
        state_size=input_size, 
        action_size=output_size, 
        lr=lr, 
        gamma=gamma,
        epsilon_start=epsilon_start, 
        epsilon_end=epsilon_end, 
        epsilon_decay=epsilon_decay
    )
    
    best_reward = float('-inf')
    best_model = None
    rewards_history = []
    
    for episode in range(episodes):
        game.generation = episode  # For display purposes
        
        # Run episode
        episode_reward = q_learning_episode(game, agent.policy_net, agent)
        rewards_history.append(episode_reward)
        
        # Track best model
        if episode_reward > best_reward:
            best_reward = episode_reward
            best_model = copy.deepcopy(agent.policy_net)
        
        # Print progress every 10 episodes
        if episode % 10 == 0:
            avg_reward = np.mean(rewards_history[-10:]) if len(rewards_history) >= 10 else np.mean(rewards_history)
            print(f"Episode {episode}/{episodes}: Avg Reward = {avg_reward:.2f}, Epsilon = {agent.epsilon:.3f}")
    
    print(f"Q-Learning training completed. Best reward: {best_reward:.2f}")
    
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
