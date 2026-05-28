from pygame.rect import Rect
from utility import *
import levelLoader
# --- Sfondo a scorrimento orizzontale ---
sfondo_originale = pygame.image.load(GamePath + "/assets/lvls/sfondolivello2.png").convert()
# Scala lo sfondo a 3x la larghezza dello schermo per permettere lo scorrimento
SFONDO_W = SCREEN_WIDTH * 3  # 3840px di larghezza
SFONDO_H = SCREEN_HEIGHT

TILE_SIZE = levelLoader.tmx_data.tilewidth           # 64
WORLD_W = levelLoader.tmx_data.width * TILE_SIZE     # 20 * 64 = 1280
WORLD_H = levelLoader.tmx_data.height * TILE_SIZE    # 12 * 64 = 768
player_pos = pygame.Vector2(WORLD_W / 2, WORLD_H / 2)  # fallback
for obj in levelLoader.tmx_data.objects:
    if obj.type == "Player":
        player_pos = pygame.Vector2(obj.x, obj.y)
        break
sfondo = pygame.transform.scale(sfondo_originale, (SFONDO_W, SFONDO_H))
SPRITE_W, SPRITE_H = 49, 57  # dimensioni sprite (usate anche dopo)
ground_rects = []   # superfici su cui atterrare (Terreno, Piattaforme, Scalino)
wall_rects = []     # muri e bordi che bloccano il movimento

for obj in levelLoader.tmx_data.objects:
    if hasattr(obj, 'width') and obj.width and obj.height:
        r = pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))
        if obj.name in ["Terreno", "Piattaforma_Bassa", "PIattaforma_Alta", "Scalino"]:
            ground_rects.append(r)
        elif obj.name in ["Muro", "Boundary_D", "Boundary_S", "Soffitto"]:
            wall_rects.append(r)
def find_ground_y(px, py):
    """Trova la superficie di atterraggio più vicina sotto al giocatore."""
    player_feet = py + SPRITE_H / 2  # bordo inferiore dello sprite
    best_y = WORLD_H  # fallback: fondo del mondo
    for rect in ground_rects:
        # Il giocatore deve essere orizzontalmente sopra la piattaforma
        if px + SPRITE_W / 2 > rect.left and px - SPRITE_W / 2 < rect.right:
            # La piattaforma deve essere sotto (o ai piedi del) giocatore
            if rect.top >= py - 10:  # piccolo margine per non perdere il contatto
                if rect.top < best_y:
                    best_y = rect.top
    # Converti dalla posizione piedi alla posizione centro sprite
    return int((best_y - SPRITE_H / 2) / 10) * 10
def collisionWalls(keys, half_w, player_rect):
    for wall in wall_rects:
        if player_rect.colliderect(wall):
            # Spingi il giocatore fuori dal muro (risoluzione orizzontale)
            if keys[pygame.K_d]:  # stava andando a destra
                player_pos.x = wall.left - half_w
            elif keys[pygame.K_a]:  # stava andando a sinistra
                player_pos.x = wall.right + half_w
#to do: fix this bs
def collisonGroundSide(keys, half_w, player_rect):
    for ground in ground_rects:
        print(ground.left)
        if player_rect.colliderect(ground):
            if keys[pygame.K_d] and Rect.collidepoint(ground.left):  # stava andando a destra
                player_pos.x = ground.left - half_w
            elif keys[pygame.K_a] and Rect.collidepoint(ground.right):  # stava andando a sinistra
                player_pos.x = ground.right + half_w
                
def collisionContinuos(keys, half_w, player_rect):
    collisionWalls(keys, half_w, player_rect)
    #collisonGroundSide(keys, half_w, player_rect)
