from logging import NullHandler
from os import name
from utility import *
import utility
import enemyMan
import gameObjects
class weaponClass:
    cooldown = 0.0
    baseCooldown = 0.0
    def primaryShot(self):
        print("prim shot")

    def secondaryShot(self):
        print("second shot")

    def groundReset(self):
        #codice filler, serve per evitare che pyright rompa il cazzo con:
        #"gne perchè non ci sta un cazzo qui? errore di identazione?" 
        #NO VOGLIO SOLO UNA FUNZIONE VUOTA GRAZIE
        a = None 
    
    def shotTravel(self):
        a = None

    def shotHitbox(self):
        a = None

    def shotRender(self):
        a = None

class umbrellaClass(weaponClass):
    def __init__(self, baseCooldown) -> None:
        super().__init__()
        self.baseCooldown = baseCooldown

    def primaryShot(self):
        super().primaryShot()
        print("umbrella")

    def secondaryShot(self):
        super().secondaryShot()
        print("umbrella")

class knuckleClass(weaponClass):
    def __init__(self, baseCooldown) -> None:
        super().__init__()
        self.baseCooldown = baseCooldown
    
    def primaryShot(self):
        super().primaryShot()
        print("knuckle")

    def secondaryShot(self):
        super().secondaryShot()
        print("knucle")

        

class knifeClass(weaponClass):
    knives = []
    knifeW, knifeH = 30, 8
    knifeSurf = pygame.Surface((knifeW, knifeH), pygame.SRCALPHA)
    grapple = {
        'active': False,
        'pos': pygame.Vector2(0, 0),
        'vel': pygame.Vector2(0, 0),
        'state': 'idle', # 'idle', 'extending', 'pulling', 'attached'
        'start_x': 0,
        'target_hook': None
    }

    def __init__(self, baseCooldown) -> None:
        super().__init__()
        self.baseCooldown = baseCooldown

    
    def primaryShot(self):
        super().primaryShot()
        if self.cooldown <= 0:
            self.cooldown = self.baseCooldown
            speed_x = 800 if player.direction == "right" else -800
            self.knives.append({
                'pos': pygame.Vector2(player.player_pos.x, player.player_pos.y),
                'vel': pygame.Vector2(speed_x, 0),
                'angle': 0 if player.direction == "right" else 180,
                'angular_vel': -1080 if player.direction == "right" else 1080, # Gradi al sec
                'stuck': False,
                'stuck_timer': 0.0
            })

    def secondaryShot(self):
        super().secondaryShot()
        if not self.grapple['active']:
                self.grapple['active'] = True
                self.grapple['state'] = 'extending'
                self.grapple['pos'] = pygame.Vector2(player.player_pos.x, player.player_pos.y)
                self.grapple['start_x'] = player.player_pos.x
                self.grapple['target_hook'] = None
                
                # Auto-aim se in volo
                if not player.onGround and gameObjects.hookPoints:
                    # Trova l'hook point più vicino e più in alto nella direzione in cui guarda
                    best_hook = None
                    best_score = float('-inf')
                    for hp in gameObjects.hookPoints:
                        dist = math.hypot(hp.x - player.player_pos.x, hp.y - player.player_pos.y)
                        is_in_front = (hp.x >= player.player_pos.x) if player.direction == "right" else (hp.x <= player.player_pos.x)
                        
                        if is_in_front and dist <= 450:
                            # Punteggio: premia la minor distanza e la maggior altezza (y minore)
                            score = (450 - dist) + (player.player_pos.y - hp.y) * 1.5
                            if score > best_score:
                                best_score = score
                                best_hook = hp
                    
                    if best_hook:
                        self.grapple['target_hook'] = best_hook
                        # Calcola vettore velocità verso l'hook point
                        dir_x = best_hook.x - player.player_pos.x
                        dir_y = best_hook.y - player.player_pos.y
                        length = math.hypot(dir_x, dir_y)
                        speed_grapple = 1200
                        self.grapple['vel'] = pygame.Vector2((dir_x / length) * speed_grapple, (dir_y / length) * speed_grapple)
                    else:
                        self.grapple['vel'] = pygame.Vector2(1200 if player.direction == "right" else -1200, 0)
                else:
                    self.grapple['vel'] = pygame.Vector2(1200 if player.direction == "right" else -1200, 0)
    
    def knifeThrow(self):
        for k in self.knives[:]:
            if not k['stuck']:
                k['pos'] += k['vel'] * utility.dt
                k['angle'] += k['angular_vel'] * utility.dt
                
                # Controllo collisione col nemico
                if enemyMan.testEnemy.enemyRect.collidepoint(k['pos'].x, k['pos'].y):
                    k['stuck'] = True
                    k['stuck_timer'] = 0.7 # Rimane piantato per 0.7 secondi
                    
                # Rimuovi se esce dallo schermo
                elif k['pos'].x < 0 or k['pos'].x > SCREEN_WIDTH:
                    self.knives.remove(k)
            else:
                # Coltello piantato: gestiamo il timer per farlo sparire
                k['stuck_timer'] -= utility.dt
                if k['stuck_timer'] <= 0:
                    self.knives.remove(k)
        
    def grappleThrow(self):
        self.grapple['pos'] += self.grapple['vel'] * utility.dt
        
        # Controllo collisione col nemico
        if not self.grapple['target_hook'] and enemyMan.testEnemy.enemyRect.collidepoint(self.grapple['pos'].x, self.grapple['pos'].y):
            self.grapple['state'] = 'pulling'
            player.Falling = False
            player.playerJumping = False
            player.JumpDuration = -1
        # Controllo distanza dal target_hook
        elif self.grapple['target_hook'] and math.hypot(self.grapple['pos'].x - self.grapple['target_hook'].x, self.grapple['pos'].y - self.grapple['target_hook'].y) < 30:
            self.grapple['state'] = 'pulling'
            self.grapple['pos'].x = self.grapple['target_hook'].x
            self.grapple['pos'].y = self.grapple['target_hook'].y
            player.Falling = False
            player.playerJumping = False
            player.JumpDuration = -1
        # Controllo distanza (max 450 pixel per auto-aim) o uscita schermo
        elif abs(self.grapple['pos'].x - self.grapple['start_x']) > 450 or self.grapple['pos'].y < 0 or self.grapple['pos'].x < 0 or self.grapple['pos'].x > SCREEN_WIDTH:
            self.grapple['active'] = False
            self.grapple['state'] = 'idle'
        
    def grapplePull(self):
            # Avvicina il personaggio (in 2D verso pos)
            pull_speed = 800
            dir_x = self.grapple['pos'].x - player.player_pos.x
            dir_y = self.grapple['pos'].y - player.player_pos.y
            dist = math.hypot(dir_x, dir_y)
            
            if dist < 30:
                if self.grapple['target_hook']:
                    # Arrivato all'hook point, si appende
                    self.grapple['state'] = 'attached'
                    player.player_pos.x = self.grapple['pos'].x
                    player.player_pos.y = self.grapple['pos'].y + 20 # Si appende un po' sotto
                    player.onGround = False
                    player.Falling = False
                    player.JumpDuration = -1 # Evita che il thread di salto attivi la caduta
                    player.GravityForce = player.MinGravityForce
                else:
                    # Arrivato al nemico, si sgancia
                    self.grapple['active'] = False
                    self.grapple['state'] = 'idle'
                    player.JumpDuration = 0 # Ripristina il contatore del salto per attivare la caduta
            else:
                player.player_pos.x += (dir_x / dist) * pull_speed * utility.dt
                player.player_pos.y += (dir_y / dist) * pull_speed * utility.dt
        
    def grappleAtteched(self):
        player.player_pos.x = self.grapple['pos'].x
        player.player_pos.y = self.grapple['pos'].y + 20
    
    def shotTravel(self):
        super().shotTravel()
        self.knifeThrow()
        if self.grapple['active']:
            if self.grapple['state'] == 'extending':
                self.grappleThrow()
            elif self.grapple['state'] == 'pulling':
                self.grapplePull()
            else:
                self.grappleAtteched()

    def knivesRender(self):
        pygame.draw.rect(self.knifeSurf, (200, 200, 200), (0, 0, self.knifeW, self.knifeH)) # Lama
        pygame.draw.rect(self.knifeSurf, (139, 69, 19), (0, 0, 10, self.knifeH)) # Manico
        
        for k in self.knives:
            rotated_surf = pygame.transform.rotate(self.knifeSurf, k['angle'])
            rotated_rect = rotated_surf.get_rect(center=(int(k['pos'].x), int(k['pos'].y)))
            screen.blit(rotated_surf, rotated_rect)
        
    def grappleRender(self):
        if self.grapple['active']:
            # Corda
            pygame.draw.line(screen, (200, 200, 200), (player.player_pos.x, player.player_pos.y), (self.grapple['pos'].x, self.grapple['pos'].y), 2)
            
            # Coltello sulla punta (orientato nella direzione del tiro)
            dir_x = self.grapple['pos'].x - player.player_pos.x
            dir_y = self.grapple['pos'].y - player.player_pos.y
            if dir_x != 0 or dir_y != 0:
                angle = math.degrees(math.atan2(-dir_y, dir_x))
            else:
                angle = 0 if player.direction == "right" else 180
                
            rotated_hook_surf = pygame.transform.rotate(self.knifeSurf, angle)
            rotated_hook_rect = rotated_hook_surf.get_rect(center=(int(self.grapple['pos'].x), int(self.grapple['pos'].y)))
            screen.blit(rotated_hook_surf, rotated_hook_rect)

    def shotRender(self):
        super().shotRender()
        self.knivesRender()
        self.grappleRender()

        

    def hookDetachJump(self):
        self.grapple['active'] = False
        self.grapple['state'] = 'idle'
        player.speed = player.baseSpeed + 50
        player.playerJumping = True
        player.JumpDuration = player.MaxJumpDuration
        player.JumpForce = player.MaxJumpForce
        player.Falling = False
        player.momentumX = 400 if player.direction == "right" else -400 # Boost direzionale
    
    def hookCancelJump(self):
        self.grapple['active'] = False
        self.grapple['state'] = 'idle'
        player.speed = player.baseSpeed + 50
        player.playerJumping = True
        player.JumpDuration = player.MaxJumpDuration
        player.JumpForce = player.MaxJumpForce
        player.direction = "right" if self.grapple['pos'].x >= player.player_pos.x else "left"
        player.Falling = False
        player.momentumX = 800 if player.direction == "right" else -800 # Boost direzionale
    

class shotgunClass(weaponClass):
    bullets = []
    shots = []
    hasDoubleJumped = False
    hasRecoveryJumped = False
    isShotgunJump = False
    def __init__(self, baseCooldown):
        self.baseCooldown = baseCooldown
    def primaryShot(self): #pyright: ignore
        super().primaryShot()
        if self.cooldown <= 0:
            self.cooldown = self.baseCooldown
            newShot = {'origin': pygame.Vector2(player.player_pos.x, player.player_pos.y), 'type': 'horizontal', 'bullets': []}
            for _ in range(5):
                speed_x = 1000 if player.direction == "right" else -1000
                speed_y = random.uniform(-200, 200) 
                b = {
                    'pos': pygame.Vector2(player.player_pos.x, player.player_pos.y),
                    'vel': pygame.Vector2(speed_x, speed_y),
                    'lifetime': 0.3 
                }
                self.bullets.append(b)
                newShot['bullets'].append(b)
                self.shots.append(newShot)

    def secondaryShot(self):
        super().secondaryShot()
        if not player.onGround and not self.hasDoubleJumped or not self.hasRecoveryJumped:
            self.hasDoubleJumped = True # Segna che ha già usato il doppio salto
            self.hasRecoveryJumped = True
            # Genera 5 pallini verso il basso e registra il colpo
            newShot = {'origin': pygame.Vector2(player.player_pos.x, player.player_pos.y), 'type': 'vertical', 'bullets': []}
            for _ in range(5):
                speed_x = random.uniform(-200, 200) # Dispersione orizzontale
                speed_y = 1000 # Proiettili verso il basso
                b = {
                    'pos': pygame.Vector2(player.player_pos.x, player.player_pos.y),
                    'vel': pygame.Vector2(speed_x, speed_y),
                    'lifetime': 0.3
                }
                self.bullets.append(b)
                newShot['bullets'].append(b)
            self.shots.append(newShot)
                
            # LOGICA DEL DOPPIO SALTO
            player.Falling = False
            player.onGround = False
            player.playerJumping = True
            self.isShotgunJump = True # Bypass controllo barra spaziatrice
            player.JumpDuration = player.MaxJumpDuration
            player.JumpForce = player.MaxJumpForce # Spinta verso l'alto
            player.GravityForce = player.MinGravityForce
        

    def groundReset(self):
        super().groundReset()
        self.hasDoubleJumped = False
        self.hasRecoveryJumped = False
        self.isShotgunJump = False

    def shotTravel(self):
        super().shotTravel()
        for b in self.bullets[:]:
            b['pos'] += b['vel'] * utility.dt
            b['lifetime'] -= utility.dt
            if b['lifetime'] <= 0 or b['pos'].x < 0 or b['pos'].x > utility.SCREEN_WIDTH:
                self.bullets.remove(b)

    def shotHitbox(self):
        super().shotHitbox()
        for shot in self.shots[:]:
            # Rimuovi i proiettili scaduti dal colpo
            shot['bullets'] = [b for b in shot['bullets'] if b in self.bullets]
            
            # Se non ci sono più proiettili, il colpo è finito
            if not shot['bullets']:
                self.shots.remove(shot)
                continue
                
            # Calcola i punti del poligono (cono con base a larghezza fissa)
            HITBOX_WIDTH = 80 # Puoi cambiare questo valore per modificare l'ampiezza della base del cono
            half_w = HITBOX_WIDTH / 2
            origin = shot['origin']
            
            if shot['type'] == 'horizontal':
                front_x = shot['bullets'][0]['pos'].x
                shot['hitbox'] = [
                    (int(origin.x), int(origin.y)), 
                    (int(front_x), int(origin.y - half_w)), 
                    (int(front_x), int(origin.y + half_w))
                ]
            else:
                front_y = shot['bullets'][0]['pos'].y
                shot['hitbox'] = [
                    (int(origin.x), int(origin.y)), 
                    (int(origin.x - half_w), int(front_y)), 
                    (int(origin.x + half_w), int(front_y))
                ]
        
    def shotRender(self):
        super().shotRender() 
        for shot in self.shots:
            if 'hitbox' in shot:
                points = shot['hitbox']
                lx, ly = zip(*points)
                min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
                
                width = max(1, max_x - min_x)
                height = max(1, max_y - min_y)
                
                shape_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.polygon(shape_surf, (255, 100, 0, 80), [(x - min_x, y - min_y) for x, y in points])
                screen.blit(shape_surf, (min_x, min_y))
                
                # Disegna anche un contorno
                pygame.draw.polygon(screen, (255, 150, 0), points, 1)

        # Disegna i proiettili
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (int(b['pos'].x), int(b['pos'].y)), 4)


knifeC = knifeClass(0.3)
shotgunC = shotgunClass(0.5)
knucklesC = knuckleClass(0.1)
umbrellaC = umbrellaClass(0.1)
class playerChar:
    name = ""
    playerClass = ("knife", knifeC)
    classes = [("knife", knifeC), ("shotgun", shotgunC), ("umbrella", umbrellaC), ("knuckles", (knucklesC))]
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
    player_rect = NullHandler
    player_pos = pygame.Vector2(0, 0)
    direction = ""
    momentumX = 0.0

    def switchClassShortCut(self, keys):

        prevClass = self.playerClass
        if keys[pygame.K_1]:
            self.playerClass = self.classes[0]    
        elif keys[pygame.K_2]:
            self.playerClass = self.classes[1]    
        elif keys[pygame.K_3]:
            self.playerClass = self.classes[2]    
        elif keys[pygame.K_4]:
            self.playerClass = self.classes[3]

        if isinstance(prevClass[1], knifeClass) and prevClass != self.playerClass:
            print("whatsapp mark")
            knifeC.grapple['active'] = False
            knifeC.grapple['state'] = 'idle'

    def switchClass(self, Next = True):
        prevClass = self.playerClass
        curInd = self.classes.index(self.playerClass)
        if Next and curInd < 3:
            curInd += 1
        elif not Next and curInd > 0:
            curInd -= 1
        self.playerClass = self.classes[curInd]
        if isinstance(prevClass[1], knifeClass) and prevClass != self.playerClass:
            print("whatsapp mark")
            knifeC.grapple['active'] = False
            knifeC.grapple['state'] = 'idle'

    def momentumHandler(self):
        if abs(self.momentumX) > 0:
            self.player_pos.x += self.momentumX * dt
            sign = 1 if self.momentumX > 0 else -1
            self.momentumX -= sign * 1500 * dt # Decelerazione
            if (sign == 1 and self.momentumX < 0) or (sign == -1 and self.momentumX > 0):
                self.momentumX = 0
        




player = playerChar() 

