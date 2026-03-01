import sys
import pygame
from src.Infrastructure.Container import Container
def main():
    container = Container()
    game = container.create_app()
