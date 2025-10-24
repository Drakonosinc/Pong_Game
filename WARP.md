# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

- Setup (venv) and install deps
```bash path=null start=null
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install --upgrade pip
pip install pygame torch numpy  # TensorFlow is optional; only needed if you switch the model backend
```

- Run the game (entry point)
```bash path=null start=null
python src/Main.py
```

- Assets and config locations used at runtime
```bash path=null start=null
Config/config.json    # gameplay, AI, visuals, key bindings
images/               # backgrounds, planets, ships
sounds/               # SFX/music
AI/best_model.pth     # optional pretrained model auto-loaded if present
```

- Training and saving
  - Choose mode in the UI: Main Menu → “Press To Start” → Game Mode → select “Training AI” then pick “Genetic” or “Q-learning”, adjust hyperparameters, Continue.
  - Press 1 during gameplay to save the current model to AI/best_model.pth if “Save model” is ON.

- Linting/tests
  - No linter or test suite is configured in this repo.

## Architecture overview

- Entry and control flow
  - src/Main.py runs an infinite loop of game sessions. After each session it branches:
    - Training AI: runs genetic_algorithm(...) or q_learning_algorithm(...) based on Config/config.json → config_AI.type_training.
    - Player or AI modes: calls Space_pong_game.run_with_model() using a loaded/trained model.

- Game loop and mechanics
  - src/Game/Space_Pong.py defines Space_pong_game (inherits from Interface.interface): initializes assets/UI, handles events, draws frames, updates physics, scores, and mode transitions. Uses Entities.Player and Entities.Ball for paddles/balls.

- UI framework and menus
  - src/Interface/Interface.py composes menus and shared element factories.
  - src/Interface/Elements_interface.py implements reusable UI primitives (Text, TextButton, PolygonButton, Input_text, ScrollBar, ComboBox) with hover/press behavior.
  - src/Interface/Menus/* implement screens: Main menu, Game mode (select mode, hyperparameters, backend, save toggle), Options (sound, visuals, keys), Pause, Game Over.

- Configuration, assets, and loading
  - src/Loaders/Config_Loader.py reads/writes Config/config.json; sets defaults if missing.
  - src/Loaders/Load_elements.py initializes pygame, fonts, sounds, images, window; auto-loads AI/best_model.pth if found.

- AI integration
  - src/AI/AI_Controller.py defines AIHandler: builds a 6-dim game state [p1x,p1y,p2x,p2y,ballx,bally] and applies actions each frame.
    - Genetic mode: forward(model(state)) → continuous action mapped to UP/DOWN.
    - Q-learning mode: delegates to a global trainer (_qlearning_trainer) to store transitions and choose discrete actions (0=UP,1=DOWN).

- Models and training backends
  - src/Type_Model/Neural_Network_Pytorch.py defines SimpleNN (PyTorch) and exports by default via src/Type_Model/__init__.py.
  - src/Type_Model/Neural_Network_Tensorflow.py provides an alternative SimpleNN, but switching requires editing __init__.py and adapting save/load (current save/load utilities use torch.save/load).
  - src/Type_Training/Genetic_Algorithm.py implements evolution over SimpleNN parameters; fitness is game.run_with_model() reward; includes save_model/load_model (PyTorch).
  - src/Type_Training/Q_learning.py implements a DQN (ReplayMemory, policy/target nets) with a QLearningTrainer that reuses the game loop; includes save/load helpers.

## Notes and caveats

- Package layout: src is not a Python package root (no src/__init__.py); run with `python src/Main.py` rather than `python -m src.Main`.
- Backend toggle: The UI exposes “Pytorch/Tensorflow”, but the code exports PyTorch by default; TensorFlow mode is not wired end-to-end (saving/loading uses torch). Use PyTorch unless you intend to refactor.
- Case sensitivity: AI/__init__.py imports `Ai_Controller` while the file is `AI_Controller.py`; this works on Windows but will fail on case-sensitive filesystems.
- requirements.txt is empty; install pygame, torch, numpy manually (see Commands).
