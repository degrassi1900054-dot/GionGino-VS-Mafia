from utility import * 
from levelLoader import *
import levelLoader
from terrainMan import * 
import terrainMan

pygame.init()
player_pos = terrainMan.player_pos
loadLevel("test")

#Path dell drectory di base del Gioco
clock = pygame.time.Clock()

# --- Sfondo a scorrimento orizzontale ---

# Posizione del giocatore nel mondo (coordinate mondo)
GroundY = find_ground_y(player_pos.x, player_pos.y)
player_pos.y = GroundY
# Offset della telecamera: il personaggio appare a 1/4 dallo schermo sinistro
CAMERA_OFFSET_X = SCREEN_WIDTH // 4  # ~320px dal bordo sinistro
CAMERA_OFFSET_Y = SCREEN_HEIGHT // 2
running = True   
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
dt = 0
def setGroundY():
    global GroundY
    GroundY = find_ground_y(player_pos.x, player_pos.y)
def setDt(delta):
    global dt
    dt = delta
#funzione di de-fanculizazione dei valori riguardante la fisica di gioco, perche` ovviamente ci sta bisogno di una stronzata del genere
def PhysicsNormalizer(number):
    number /= 10
    number = int(number)
    number*=10
    return number
#funzione fisica del salto, alcuni dettagli andranno modificati per accomodare interazioni con eventuali piattaforme
def jump():
    global onGround
    global JumpForce
    global playerJumping
    global JumpDuration
    global Falling
    global GravityForce
    global player_pos
    global dt
    while True:
        if playerJumping and JumpDuration > 0:
            onGround = False
            player_pos.y -= math.floor(JumpForce * dt) 
            JumpDuration -= 1 
            if JumpDuration > 45:
                JumpForce -= math.floor(60 * dt) 
            elif JumpDuration > 40:
                JumpForce -= math.floor(50 * dt) 
            elif JumpDuration > 35:
                JumpForce -= math.floor(40 * dt) 
            elif JumpDuration > 30:
                JumpForce -= math.floor(30 * dt) 
        elif JumpDuration == 0:
            if not Falling:
                Falling = True
                GravityForce = MinGravityForce
                playerJumping = False
        time.sleep(0.003)
#funzione fisica caduta, guarda nota funzione salto            
def fall(): 
    global onGround
    global Falling
    global GroundY
    global player_pos
    global GravityForce
    global dt
    while True:
        time.sleep(0.01)
        setGroundY()
        if Falling and GroundY > player_pos.y:
            player_pos.y += math.floor(GravityForce * dt)
            GravityForce += 10
        elif int(GroundY) <= int(player_pos.y):
            player_pos.y = GroundY
            Falling = False
            onGround = True
            GravityForce = MinGravityForce

def movementInHandler(keys):
    global Falling
    global speed
    global baseSpeed
    global onGround
    global playerJumping
    global GravityForce
    global MinGravityForce
    global JumpDuration
    global MaxJumpDuration
    global JumpForce
    global MaxJumpForce
    global player_pos
    global dt
    if keys[pygame.K_SPACE] and not Falling:
        speed = baseSpeed + 50 #velocita` lergemente piu` alta durante il salto, per dare idea di slancio in avanti e di rincorsa
        playerJumping = True
        if onGround:
            JumpDuration = MaxJumpDuration
            JumpForce = MaxJumpForce
    else:
        speed = baseSpeed
        playerJumping = False
        if not Falling:
            Falling = True
            GravityForce = MinGravityForce
    if keys[pygame.K_d]:
        player_pos.x += speed * dt
    elif keys[pygame.K_a]:
        player_pos.x -= speed * dt
JumpThread = threading.Thread(target=jump, daemon=True) 
FallThread = threading.Thread(target=fall, daemon=True)
JumpThread.start()
FallThread.start()
