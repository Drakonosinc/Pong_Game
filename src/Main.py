import sys
from pathlib import Path
SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
for path in (PROJECT_ROOT, SRC_ROOT):
    path_str = str(path)
    if path_str not in sys.path: sys.path.insert(0, path_str)
from src.Infrastructure.Container import Container
def main():
    container = Container()
    game = None
    try:
        game = container.create_app()
        while True:
            game.run()
            if game.exit: break
            game.game_over = False
            if game.mode_game["Training AI"]:
                trainer = container.get_trainer()
                best_model = trainer.train(game)
                if game.exit: break
                game.model = best_model
                if best_model: 