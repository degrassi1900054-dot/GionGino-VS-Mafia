from utility import *
from movement import *
from levelLoader import *
keys = NullHandler
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    setDt(dt)
    movementInHandler(keys)


    # --- Calcolo posizione telecamera ---
    # La telecamera cerca di posizionare il giocatore a CAMERA_OFFSET_X dal bordo sinistro
    camera_x = player_pos.x - CAMERA_OFFSET_X
    
    # Limita la telecamera ai bordi dello sfondo
    camera_x = max(0, camera_x)                         # Non andare oltre il bordo sinistro
    camera_x = min(camera_x, SFONDO_W - SCREEN_WIDTH)   # Non andare oltre il bordo destro
    
    # Disegna lo sfondo con offset della telecamera
    screen.blit(sfondo, (-camera_x, 0))
    drawLevel()


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
    #input direzione
    
    # Limita il giocatore ai bordi del mondo (sfondo)
    half_w = dimensioni_sprite[0] / 2
    player_pos.x = max(half_w, player_pos.x)
    player_pos.x = min(SFONDO_W - half_w, player_pos.x)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
