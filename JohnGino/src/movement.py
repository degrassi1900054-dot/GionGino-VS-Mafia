from utility import * 
import utility
from levelLoader import *
import levelLoader
from terrainMan import * 
import terrainMan
from charMan import *

pygame.init()
loadLevel("test")

#Path dell drectory di base del Gioco
clock = pygame.time.Clock()

# --- Sfondo a scorrimento orizzontale ---

# Posizione del giocatore nel mondo (coordinate mondo)
GroundY = find_ground_y(charMan.player.player_pos.x,  charMan.player.player_pos.y)
player.player_pos.y = GroundY
# Offset della telecamera: il personaggio appare a 1/4 dallo schermo sinistro
CAMERA_OFFSET_X = SCREEN_WIDTH // 4  # ~320px dal bordo sinistro
CAMERA_OFFSET_Y = SCREEN_HEIGHT // 2
def setGroundY():
    global GroundY
    GroundY = find_ground_y(player.player_pos.x, player.player_pos.y)
#funzione di de-fanculizazione dei valori riguardante la fisica di gioco, perche` ovviamente ci sta bisogno di una stronzata del genere
def PhysicsNormalizer(number):
    number /= 10
    number = int(number)
    number*=10
    return number
#funzione fisica del salto, alcuni dettagli andranno modificati per accomodare interazioni con eventuali piattaforme
def jump():
    while True:
        if charMan.player.playerJumping and charMan.player.JumpDuration > 0:
            charMan.player.onGround = False
            charMan.player.player_pos.y -= math.floor(charMan.player.JumpForce * utility.dt) 
            charMan.player.JumpDuration -= 1 
            if charMan.player.JumpDuration > 45:
                charMan.player.JumpForce -= math.floor(60 * utility.dt) 
            elif charMan.player.JumpDuration > 40:
                charMan.player.JumpForce -= math.floor(50 * utility.dt) 
            elif charMan.player.JumpDuration > 35:
                charMan.player.JumpForce -= math.floor(40 * utility.dt) 
            elif charMan.player.JumpDuration > 30:
                charMan.player.JumpForce -= math.floor(30 * utility.dt) 
            time.sleep(0.003)
        elif charMan.player.JumpDuration == 0:
            if not charMan.player.Falling:
                charMan.player.Falling = True
                charMan.player.GravityForce = charMan.player.MinGravityForce
def fall():
    while True:
        time.sleep(0.01)
        setGroundY()
        if charMan.player.Falling and GroundY > charMan.player.player_pos.y:
            charMan.player.player_pos.y += math.floor(charMan.player.GravityForce * utility.dt)
            charMan.player.GravityForce += 10
        elif int(GroundY) <= int(charMan.player.player_pos.y):
            charMan.player.player_pos.y = GroundY
            charMan.player.Falling = False
            charMan.player.onGround = True
            charMan.player.GravityForce = charMan.player.MinGravityForce

def movementInHandler(keys):
    if keys[pygame.K_SPACE] and not charMan.player.Falling:
        charMan.player.speed = charMan.player.baseSpeed + 50 #velocita` lergemente piu` alta durante il salto, per dare idea di slancio in avanti e di rincorsa
        charMan.player.playerJumping = True
        if player.onGround:
            charMan.player.JumpDuration = charMan.player.MaxJumpDuration
            charMan.player.JumpForce = charMan.player.MaxJumpForce
    else:
        charMan.player.speed = charMan.player.baseSpeed
        charMan.player.playerJumping = False
        if not charMan.player.Falling:
            charMan.player.Falling = True
            charMan.player.GravityForce = charMan.player.MinGravityForce
    if keys[pygame.K_d]:
        charMan.player.player_pos.x += player.speed * utility.dt
    elif keys[pygame.K_a]:
        charMan.player.player_pos.x -= player.speed * utility.dt
JumpThread = threading.Thread(target=jump, daemon=True) 
FallThread = threading.Thread(target=fall, daemon=True)
JumpThread.start()
FallThread.start()
