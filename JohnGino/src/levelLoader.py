from logging import NullHandler

from utility import *
from pytmx.util_pygame import load_pygame
import pygame
tmx_data = NullHandler
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
class level:
    name = ""
    path = ""
    def __init__(self, name, path):
        #nome livello
        self.name= name
        #path mappa
        self.path = path

lvlList = [level("test", GamePath + "/maps/test_area.tmx")]
def drawLevel():
    global tmx_data
    for layer in tmx_data.visible_layers:#pyright: ignore
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                screen.blit(surf, (x * 64, y *64))

def loadLevel(toLoad):
    global lvlList
    global tmx_data
    path = next(l for l in lvlList if l.name == toLoad).path
    tmx_data = load_pygame(path)
    tmx_data.get_layer_by_name("Tiles1")
loadLevel("test")

    
    

        
        
