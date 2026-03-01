import sys
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
