import unittest
from unittest.mock import MagicMock
import pygame
from pygame.locals import *
from tests import conftest

from src.Interface.Elements_interface import (
    ElementsFactory,
    Text,
    TextButton,
    PolygonButton,
    Input_text,
    ScrollBar,
    ComboBoxDown,
)
