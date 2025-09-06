# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Space Pong game implemented in Python using pygame and PyTorch. The project features:
- A classic Pong game with space-themed graphics
- AI player training using genetic algorithms
- Neural network models built with PyTorch
- Complete GUI interface with multiple game modes

## Core Architecture

### Entry Point
The application starts from `src/Main.py`, which creates a `Space_pong_game` instance and handles the main game loop including AI training cycles.

### Main Components

**Game Engine** (`src/Game/Space_Pong.py`)
- Core game logic, physics, and rendering
- Inherits from `interface` class providing UI capabilities
- Manages three game modes: Training AI, Player vs Player, Player vs AI

**AI System** (`src/AI/AI_Controller.py`)
- `AIHandler` class processes game state and executes AI actions
- State representation: player positions (x,y) and ball position (x,y)
- AI outputs control player paddle movement

**Neural Networks** (`src/Type_Model/`)
- `Neural_Network_Pytorch.py`: Simple 2-layer neural network (input -> 128 hidden -> output)
- Supports activation visualization in-game
- Alternative TensorFlow implementation available

**Training System** (`src/Type_Training/`)
- `Genetic_Algorithm.py`: Complete genetic algorithm implementation
- `Q_learning.py`: Deep Q-Network (DQN) implementation with experience replay
- Population-based evolution (Genetic) vs. experience replay (Q-learning)
- Configurable parameters for both training methods

**Interface System** (`src/Interface/`)
- Modular menu system with multiple screens (main, game over, options, etc.)
- Element factory pattern for UI components
- Sound integration and key mapping

**Configuration** (`Config/config.json`)
- Visual settings (screen size, backgrounds, sprites)
- AI parameters (generations, population, training type)
- Key bindings and game rules
- Sound settings

## Common Commands

### Running the Game
```bash
python src/Main.py
```

### Training AI Models
The AI training is integrated into the game flow. Start the game and select "Training AI" mode from the menu. Choose between Genetic Algorithm or Q-learning in `Config/config.json` by setting the appropriate `type_training` flag.

**Genetic Algorithm Parameters:**
- `generation_value`: Number of generations (default: 100)
- `population_value`: Population size (default: 20) 
- `try_for_ai`: Trials per model evaluation (default: 3)

**Q-learning Parameters:**
- `episodes`: Number of training episodes (default: 500)
- `learning_rate`: Learning rate for neural network (default: 0.001)
- `gamma`: Discount factor for future rewards (default: 0.99)
- `epsilon_start/end/decay`: Exploration parameters for epsilon-greedy policy

### Saving/Loading Models
Models are automatically saved after training if `model_save` is enabled in config. Manual save during gameplay with the `1` key. Models are stored as `AI/best_model.pth`.

## Development Notes

### Key Files to Modify

**For Game Logic Changes:**
- `src/Game/Space_Pong.py` - Main game mechanics, collision detection, scoring
- `src/Entities/` - Player and Ball behavior classes

**For AI Improvements:**
- `src/AI/AI_Controller.py` - State representation and action processing
- `src/Type_Training/Genetic_Algorithm.py` - Training algorithm parameters
- `src/Type_Model/Neural_Network_Pytorch.py` - Network architecture

**For UI Changes:**
- `src/Interface/Interface.py` and related menu classes
- `Config/config.json` - Visual and gameplay settings

### Configuration System
All major settings are externalized in `Config/config.json`. Changes to screen size, AI parameters, key bindings, and visual elements can be made without code modifications.

### AI Training Architecture

**Genetic Algorithm** creates a population of neural networks, evaluates them through gameplay, then evolves the population through:
1. **Selection**: Top performers chosen as parents
2. **Crossover**: Parameter mixing between parent networks  
3. **Mutation**: Random noise added to network weights
4. **Elitism**: Best models preserved across generations

**Q-learning (DQN)** uses reinforcement learning with experience replay:
1. **Exploration**: Epsilon-greedy action selection balances exploration vs. exploitation
2. **Experience Replay**: Transitions stored in replay buffer for batch learning
3. **Target Network**: Separate target network provides stable Q-value targets
4. **Deep Q-Network**: Neural network learns Q-values for state-action pairs

### Dependencies
- pygame (game engine)
- torch (neural networks)
- numpy (numerical operations)
- Standard library: random, copy, sys

The project uses object-oriented design with clear separation of concerns between game logic, AI systems, and user interface components.
