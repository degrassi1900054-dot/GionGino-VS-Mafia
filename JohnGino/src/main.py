from utility import *
from movement import *
from levelLoader import *
from spriteAnim import *
import utility
import charMan
import enemyMan
import gameObjects
keys = NullHandler
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                charMan.player.playerClass[1].primaryShot()
            elif event.button == 3:
                charMan.player.playerClass[1].secondaryShot()
        #ODIO PYGAME, PERCHE` E` APPARENTEMENTE QUESTO 
        #L`UNINCO MODO DI AVERE UN
        #PRESS SINGOLO INVECE DI UN HOLD?
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w:
                charMan.player.switchClass(True)
            elif event.key == pygame.K_s:
                charMan.player.switchClass(False)
            elif event.key == pygame.K_k:
                charMan.player.playerClass[1].primaryShot()
            elif event.key == pygame.K_l:
                charMan.player.playerClass[1].secondaryShot()

                    
    keys = pygame.key.get_pressed()
    setDt(dt)
    if charMan.player.playerClass[1].cooldown > 0:
        charMan.player.playerClass[1].cooldown -= dt

    if charMan.player.onGround:
        charMan.player.playerClass[1].groundReset()
    movementInHandler(keys)
    charMan.player.momentumHandler()
    charMan.player.switchClassShortCut(keys)
    
    # --- Calcolo posizione telecamera ---
    # La telecamera cerca di posizionare il giocatore a CAMERA_OFFSET_X dal bordo sinistro
    camera_x = charMan.player.player_pos.x - CAMERA_OFFSET_X
    camera_y = charMan.player.player_pos.y - CAMERA_OFFSET_Y
    
    # Limita la telecamera ai bordi del mondo
    camera_x = max(0, min(camera_x, WORLD_W - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_H - SCREEN_HEIGHT))
    
    # Disegna lo sfondo con offset della telecamera
    screen.blit(sfondo, (-camera_x, 0))
    drawLevel()


    # Determina la charMan.player.direction del giocatore
    if keys[pygame.K_d]:
        charMan.player.direction = "right"
    elif keys[pygame.K_a]:
        charMan.player.direction = "left"

    # Seleziona l'animazione corretta
    if not charMan.player.onGround:
        lista_corrente = frames_jump_dx if charMan.player.direction == "right" else frames_jump_sx
    elif keys[pygame.K_d]:
        lista_corrente = frames_walk_dx
    elif keys[pygame.K_a]:
        lista_corrente = frames_walk_sx
    else:
        lista_corrente = frames_idle_dx if charMan.player.direction == "right" else frames_idle_sx

    # Previene errori se l'indice precedente supera la lunghezza della nuova lista di frame
    if anim_index >= len(lista_corrente):
        anim_index = 0

    # 1. Prendi il frame corretto in base all'indice
    frame_corrente = lista_corrente[int(anim_index)]

    # 2. Calcola le coordinate SCHERMO per centrare il frame sulla posizione mondo del giocatore
    sprite_x = charMan.player.player_pos.x - camera_x - frame_corrente.get_width() / 2
    sprite_y = charMan.player.player_pos.y - frame_corrente.get_height() / 2

    # 3. Disegna lo sprite sullo schermo
    screen.blit(frame_corrente, (sprite_x, sprite_y))
    

    # 4. Aggiorna l'animazione
    if keys[pygame.K_d] or keys[pygame.K_a] or not charMan.player.onGround:
        anim_index += 0.15  # Velocità per camminata o salto
    else:
        anim_index += 0.05  # Velocità più lenta per lo stato fermo (idle)

    if not charMan.player.onGround:
        if anim_index >= len(lista_corrente):
            anim_index = 4  # Loop in salto (dal quinto sprite in poi)
    elif anim_index >= len(lista_corrente):
        anim_index = 0

    

    
    # Limita il giocatore ai bordi del mondo (sfondo)
    half_w = dimensioni_sprite[0] / 2
    half_h = dimensioni_sprite[1] / 2
    charMan.player.player_rect = pygame.Rect(
            charMan.player.player_pos.x - half_w, charMan.player.player_pos.y - half_h,
        dimensioni_sprite[0], dimensioni_sprite[1]
        )
    charMan.player.player_pos.x = max(half_w, charMan.player.player_pos.x)
    charMan.player.player_pos.x = min(SFONDO_W - half_w, charMan.player.player_pos.x)
    onCollisionEnter(keys)
    onCollisionStay(keys, half_w)
    
    charMan.player.playerClass[1].shotTravel()
    charMan.player.playerClass[1].shotHitbox()
    charMan.player.playerClass[1].shotRender()
    for hp in gameObjects.hookPoints:
        pygame.draw.polygon(screen, (255, 0, 255), [(hp.x, hp.y - 10), (hp.x - 10, hp.y + 10), (hp.x + 10, hp.y + 10)])
    pygame.draw.rect(screen, (50, 50, 200), enemyMan.testEnemy.enemyRect)
    #modo temporaneo per chiudere il gioco
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
