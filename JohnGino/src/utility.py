import os
from pathlib import Path
import pygame
import threading
import time 
import math
import asyncio

GamePath = str(Path(os.path.dirname(__file__)).parent.absolute())
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def chekIfAllFalse(List = []):
    allFalse = True
    for e in List:
        if(e):
            allFalse = False
            break
    return allFalse

