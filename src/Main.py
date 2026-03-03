import sys
from pathlib import Path
SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
for path in (PROJECT_ROOT, SRC_ROOT):
    path_str = str(path)

import pygame
from src.Infrastructure.Container import Container
def main():
    container = Container()
    game = container.create_app()
    while True:
        game.run()
        game.game_over = False
        if game.mode_game["Training AI"]:
            trainer = container.get_trainer()
            best_model = trainer.train(game)
            game.model = best_model
            if best_model:
                container.wrap_trained_model(best_model)
        elif game.mode_game["Player"] or game.mode_game["AI"]:
            game.run_with_model()
        if game.exit:
            break
    pygame.quit()
    sys.exit()
if __name__ == "__main__": main()