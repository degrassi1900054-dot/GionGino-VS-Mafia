import pygame
import threading
import time 
import math
import os
from pathlib import Path
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Path dell drectory di base del Gioco
GamePath = str(Path(os.path.dirname(__file__)).parent.absolute())
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

# Offset della telecamera: il personaggio appare a 1/4 dallo schermo sinistro
CAMERA_OFFSET_X = SCREEN_WIDTH // 4  # ~320px dal bordo sinistro
dt = 0
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
    while running:
        if playerJumping == True and JumpDuration > 0:
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
    while running:
        time.sleep(0.01)
        if Falling == True and GroundY > player_pos.y:
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

#sezione "update"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Calcolo posizione telecamera ---
    # La telecamera cerca di posizionare il giocatore a CAMERA_OFFSET_X dal bordo sinistro
    camera_x = player_pos.x - CAMERA_OFFSET_X
    
    # Limita la telecamera ai bordi dello sfondo
    camera_x = max(0, camera_x)                         # Non andare oltre il bordo sinistro
    camera_x = min(camera_x, SFONDO_W - SCREEN_WIDTH)   # Non andare oltre il bordo destro
    
    # Disegna lo sfondo con offset della telecamera
    screen.blit(sfondo, (-camera_x, 0))

    keys = pygame.key.get_pressed()

    # Determina la direzione del giocatore
    if keys[pygame.K_d]:
        direzione = "destra"
    elif keys[pygame.K_a]:
        direzione = "sinistra"

    # Seleziona l'animazione corretta
    if not onGround:
        lista_corrente = frames_jump_dx if direzione == "destra" else frames_jump_sx
    elif keys[pygame.K_d]:
        lista_corrente = frames_walk_dx
    elif keys[pygame.K_a]:
        lista_corrente = frames_walk_sx
    else:
        lista_corrente = frames_idle_dx if direzione == "destra" else frames_idle_sx

    # Previene errori se l'indice precedente supera la lunghezza della nuova lista di frame
    if anim_index >= len(lista_corrente):
        anim_index = 0

    # 1. Prendi il frame corretto in base all'indice
    frame_corrente = lista_corrente[int(anim_index)]

    # 2. Calcola le coordinate SCHERMO per centrare il frame sulla posizione mondo del giocatore
    sprite_x = player_pos.x - camera_x - frame_corrente.get_width() / 2
    sprite_y = player_pos.y - frame_corrente.get_height() / 2

    # 3. Disegna lo sprite sullo schermo
    screen.blit(frame_corrente, (sprite_x, sprite_y))

    # 4. Aggiorna l'animazione
    if keys[pygame.K_d] or keys[pygame.K_a] or not onGround:
        anim_index += 0.15  # Velocità per camminata o salto
    else:
        anim_index += 0.05  # Velocità più lenta per lo stato fermo (idle)

    if not onGround:
        if anim_index >= len(lista_corrente):
            anim_index = 4  # Loop in salto (dal quinto sprite in poi)
    elif anim_index >= len(lista_corrente):
        anim_index = 0

    #input salto(base)
    if keys[pygame.K_SPACE]:
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
    #input direzione
    if keys[pygame.K_d]:
        player_pos.x += speed * dt
    elif keys[pygame.K_a]:
        player_pos.x -= speed * dt
    
    # Limita il giocatore ai bordi del mondo (sfondo)
    half_w = dimensioni_sprite[0] / 2
    player_pos.x = max(half_w, player_pos.x)
    player_pos.x = min(SFONDO_W - half_w, player_pos.x)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()

