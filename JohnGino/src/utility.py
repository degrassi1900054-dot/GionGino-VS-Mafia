import os
from pathlib import Path
import pygame
import threading
import time 
import math
import random
import sys
import asyncio

GamePath = str(Path(os.path.dirname(__file__)).parent.absolute())
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True   
dt = 0
def setDt(delta):
    global dt
    dt = delta
def chekIfAllFalse(List = []):
    allFalse = True
    for e in List:
        if(e):
            allFalse = False
            break
    return allFalse
#versione per int di isClose
def isCloseInt(a, b, leniency):
    return a <= b + leniency and a >= b - leniency 
