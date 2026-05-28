from utility import *

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
