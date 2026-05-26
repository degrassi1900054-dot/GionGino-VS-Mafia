from pygame import key
from utility import * 
from levelLoader import *

pygame.init()


#Path dell drectory di base del Gioco
clock = pygame.time.Clock()

# --- Sfondo a scorrimento orizzontale ---
sfondo_originale = pygame.image.load(GamePath + "/assets/lvls/sfondolivello2.png").convert()
# Scala lo sfondo a 3x la larghezza dello schermo per permettere lo scorrimento
SFONDO_W = SCREEN_WIDTH * 3  # 3840px di larghezza
SFONDO_H = SCREEN_HEIGHT
sfondo = pygame.transform.scale(sfondo_originale, (SFONDO_W, SFONDO_H))

# Posizione del giocatore nel mondo (coordinate mondo)
player_pos = pygame.Vector2(SFONDO_W / 2, SCREEN_HEIGHT / 2)

GroundY = player_pos.y

loadLevel("test")
# Offset della telecamera: il personaggio appare a 1/4 dallo schermo sinistro
CAMERA_OFFSET_X = SCREEN_WIDTH // 4  # ~320px dal bordo sinistro
running = True
    
playerJumping = False
onGround = True
MaxJumpForce = 200
JumpForce = 0
MaxJumpDuration = 50
JumpDuration = 0
MinGravityForce = 10
GravityForce = MinGravityForce
Falling = False
baseSpeed = 300
speed = baseSpeed
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
        if Falling and GroundY > player_pos.y:
            player_pos.y += math.floor(GravityForce * dt)
            GravityForce += 10
        elif GroundY == PhysicsNormalizer(player_pos.y):
            player_pos.y = GroundY
            Falling = False
            onGround = True
            GravityForce = MinGravityForce

spritesheet = pygame.image.load(GamePath + "/assets/chars/Movement_render1.png").convert_alpha()

def separazione_spritesheet(spritesheet, n_tagli, dimensioni_sprite, riga=0):
    # n_tagli = numero di frame in quella riga
    # riga = la riga dello spritesheet da tagliare (0, 1, 2, 3...)
    frames = []
    larghezza_sprite = dimensioni_sprite[0]
    altezza_sprite = dimensioni_sprite[1]
    
    # Calcoliamo la Y iniziale per la riga selezionata
    y = riga * altezza_sprite
    
    for i in range(n_tagli):
        # Calcoliamo la X del frame i-esimo
        x = i * larghezza_sprite
        
        # Ritagliamo la porzione usando subsurface
        rettangolo = pygame.Rect(x, y, larghezza_sprite, altezza_sprite)
        frame = spritesheet.subsurface(rettangolo)
        frames.append(frame)
        
    return frames

            
JumpThread = threading.Thread(target=jump, daemon=True) 
FallThread = threading.Thread(target=fall, daemon=True)
JumpThread.start()
FallThread.start()

# Creiamo le prime 3 righe di animazione dallo spritesheet
dimensioni_sprite = (49, 57)

# Riga 0: Idle (Fermo) - 8 frame (originale rivolto a sinistra, specchiato a destra per dx)
frames_idle_sx = separazione_spritesheet(spritesheet, 8, dimensioni_sprite, riga=0)
frames_idle_dx = [pygame.transform.flip(f, True, False) for f in frames_idle_sx]

# Riga 1: Movimento a sinistra (8 frame) - specchiata a destra
frames_walk_sx = separazione_spritesheet(spritesheet, 8, dimensioni_sprite, riga=1)
frames_walk_dx = [pygame.transform.flip(f, True, False) for f in frames_walk_sx]

# Riga 2: Salto (8 frame) (originale rivolto a sinistra)
frames_jump_sx = separazione_spritesheet(spritesheet, 8, dimensioni_sprite, riga=2)
frames_jump_dx = [pygame.transform.flip(f, True, False) for f in frames_jump_sx]

anim_index = 0
direzione = "destra" # Direzione iniziale
def movementInHandler(keys, delta):
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
    dt = delta
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
        player_pos.x += speed * delta
    elif keys[pygame.K_a]:
        player_pos.x -= speed * delta
#sezione "update"
