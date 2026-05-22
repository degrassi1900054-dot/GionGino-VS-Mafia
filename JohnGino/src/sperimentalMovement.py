import math
import threading
import time
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
GroundY =  player_pos.y
dt = 0
running = True
playerJumping = False
onGround = True
Falling = False
baseSpeed = 300
speed = baseSpeed
GravityForce = 9.81 * 300 #
JumpForce = 0  
VelocityY_fall = 0 
MaxJumpForce = 200 #altezza in pixel del salto
jump_velocity_initial = math.sqrt(2 * GravityForce * MaxJumpForce)

THREAD_DT = 0.01



def jump():
    global onGround
    global JumpForce
    global playerJumping
    global Falling
    global VelocityY_fall
    global player_pos
    while True:

        if playerJumping and onGround:
            onGround = False
   
            JumpForce = jump_velocity_initial

     
        if not onGround and JumpForce > 0 and not Falling:
            # Applichiamo la gravità e cacoliamo la velocità di salita
            JumpForce -= GravityForce * THREAD_DT
            # calcoliamo la posizione y 
            player_pos.y -= JumpForce * THREAD_DT

            # all altezza massima significa che la velocità del corpo è nulla e si deve invertire di segno 
            if JumpForce <= 0:
                JumpForce = 0
                Falling = True

        time.sleep(THREAD_DT)


def fall():
    global onGround 
    global Falling 
    global GroundY 
    global player_pos
    global VelocityY_fall 
    global JumpForce
    while True:
        time.sleep(THREAD_DT)
        if Falling and player_pos.y < GroundY:
            
            VelocityY_fall += GravityForce * THREAD_DT
           
            player_pos.y += VelocityY_fall * THREAD_DT #stesso discorso del salto

        # Controllo collisione con il terreno
        if player_pos.y >= GroundY:
            player_pos.y = GroundY
            Falling = False
            onGround = True
            VelocityY_fall = 0
            JumpForce = 0


# Avvio dei Thread
JumpThread = threading.Thread(target=jump)
FallThread = threading.Thread(target=fall)
JumpThread.start()
FallThread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")  #sostituire con sfondo
 
    pygame.draw.circle(screen, "red", player_pos, 40)#sostituire con l'unico e solo John Gino


    keys = pygame.key.get_pressed()

    # Input salto(base)
    if keys[pygame.K_SPACE]:
        speed = baseSpeed + 50 #velocita` lergemente piu` alta durante il salto, per dare idea di slancio in avanti e di rincorsa
        if onGround:
            playerJumping = True
    else:
        speed = baseSpeed
        playerJumping = False
       
        if not onGround and JumpForce == 0:
            Falling = True

    # Input direzione
    if keys[pygame.K_d]:
        player_pos.x += speed * dt
    elif keys[pygame.K_a]:
        player_pos.x -= speed * dt

    pygame.display.flip()

    # dt usato solo per lo spostamento orizzontale 
    dt = clock.tick(60) / 1000

pygame.quit()