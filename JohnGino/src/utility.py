import os
from pathlib import Path
import pygame
import threading
import time 
import math

GamePath = str(Path(os.path.dirname(__file__)).parent.absolute())
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
dt = 0
