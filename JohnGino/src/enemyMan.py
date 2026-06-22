from utility import *
import utility

#classe nemici base
class enemy:
    enemyRect = pygame.Rect(0, 0, 0, 0)
    MaxHP = 0
    HP = 0
    ATK = 0
    state = {
        "normal" : (50, 50, 200),
        "hit" : (255, 255, 255),
        "hitTimer" : 0.0,
        "hitDuration" : 0.2
    }
   

testEnemy = enemy()
