from logging import NullHandler
from os import name
from utility import *
class weaponClass:
    cooldown = 0
    baseCooldown = 0
    def primaryShot(self):
        print("prim shot")

    def secondaryShot(self):
        print("second shot")

class umbrellaClass(weaponClass):
    def primaryShot(self):
        super().primaryShot()
        print("umbrella")

    def secondaryShot(self):
        super().secondaryShot()
        print("umbrella")

class knuckleClass(weaponClass):
    def primaryShot(self):
        super().primaryShot()
        print("knuckle")

    def secondaryShot(self):
        super().secondaryShot()
        print("knucle")

class knifeClass(weaponClass):
    def primaryShot(self):
        super().primaryShot()
        print("knife")

    def secondaryShot(self):
        super().secondaryShot()
        print("knife")

class shotgunClass(weaponClass):
    def primaryShot(self):
        super().primaryShot()
        print("shotgun")

    def secondaryShot(self):
        super().secondaryShot()
        print("shotgun")

knifeC = knifeClass()
shotgunC = shotgunClass()
knucklesC = knuckleClass()
umbrellaC = umbrellaClass()
class playerChar:
    name = ""
    playerClass = ("knife", knifeC)
    classes = [("knife", knifeC), ("shotgun", shotgunC), ("umbrella", umbrellaC), ("knuckles", (knucklesC))]
    playerJumping = False
    onGround = True
    MaxJumpForce = 200
    JumpForce = 0
    MaxJumpDuration = 50
    JumpDuration = 999
    MinGravityForce = 10
    GravityForce = MinGravityForce
    Falling = False
    baseSpeed = 300
    speed = baseSpeed
    player_rect = NullHandler
    player_pos = pygame.Vector2(0, 0)
    
    def switchClassShortCut(self, keys):
    
        if keys[pygame.K_1]:
            self.playerClass = self.classes[0]    
        elif keys[pygame.K_2]:
            self.playerClass = self.classes[1]    
        elif keys[pygame.K_3]:
            self.playerClass = self.classes[2]    
        elif keys[pygame.K_4]:
            self.playerClass = self.classes[3]    

    def switchClass(self, Next = True):
        curInd = self.classes.index(self.playerClass)
        if Next and curInd < 3:
            curInd += 1
        elif not Next and curInd > 0:
            curInd -= 1
        self.playerClass = self.classes[curInd]




player = playerChar() 

