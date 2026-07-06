import pygame
from settings import SCREEN_WIDTH, RED


class LevelReader:
    def __init__(self, lvl, floor_y):
        self.floor_y = floor_y
        self.score = 0
        self.world_offset = 0 
        self.game_speed = lvl.lvl_speed
        self.obstacles = [] 
        self.ceil_obstacles = [] 
        self.platforms = [] 
        self.slabs = [] 
        self.dj_orbs = [] 
        self.gr_orbs = [] 
        
        self.bg_image = pygame.transform.scale(lvl.bg_image, (SCREEN_WIDTH, self.floor_y + 50))
        self.bg_x1 = lvl.bg_x1
        self.bg_x2 = lvl.bg_x2
        self.bg_speed = lvl.bg_speed
        
        pygame.mixer.music.load(lvl.music_name)
        
        BLOCK_SIZE = 40 
        START_OFFSET = 0 
        
        self.dj_orb_texture = pygame.image.load("media/textures/double_jump.png").convert_alpha()
        self.dj_orb_texture = pygame.transform.scale(self.dj_orb_texture, (BLOCK_SIZE, BLOCK_SIZE))
        
        self.gr_orb_texture = pygame.image.load("media/textures/gravity_orb.png").convert_alpha()
        self.gr_orb_texture = pygame.transform.scale(self.gr_orb_texture, (BLOCK_SIZE, BLOCK_SIZE))

        for row_index, row in enumerate(lvl.map):
            for col_index, char in enumerate(row):
                x = START_OFFSET + (col_index * BLOCK_SIZE)
                y = row_index * BLOCK_SIZE
                
                if char == "P":
                    self.platforms.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "X":
                    self.obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "M":
                    self.ceil_obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "S":
                    self.slabs.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE // 2))
                elif char == "D":
                    self.dj_orbs.append(pygame.Rect(x, y, BLOCK_SIZE + 5, BLOCK_SIZE + 5))
                elif char == "G":
                    self.gr_orbs.append(pygame.Rect(x, y, BLOCK_SIZE + 5, BLOCK_SIZE + 5))

    def update(self):
        # Движение фона
        self.bg_x1 -= self.bg_speed
        self.bg_x2 -= self.bg_speed
        if self.bg_x1 <= -SCREEN_WIDTH:
            self.bg_x1 = self.bg_x2 + SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH:
            self.bg_x2 = self.bg_x1 + SCREEN_WIDTH
        
        self.world_offset += self.game_speed
        self.score += self.game_speed 
        
        # ИСПРАВЛЕНО: Сдвиг объектов и очистка вынесены из циклов (ОГРОМНЫЙ БУСТ FPS)
        for spike in self.obstacles: spike.x -= self.game_speed
        self.obstacles = [s for s in self.obstacles if s.right > 0]

        for c_spike in self.ceil_obstacles: c_spike.x -= self.game_speed
        self.ceil_obstacles = [s for s in self.ceil_obstacles if s.right > 0]

        for plat in self.platforms: plat.x -= self.game_speed
        self.platforms = [p for p in self.platforms if p.right > 0]

        for slab in self.slabs: slab.x -= self.game_speed
        self.slabs = [s for s in self.slabs if s.right > 0]

        for orb in self.dj_orbs: orb.x -= self.game_speed
        self.dj_orbs = [orb for orb in self.dj_orbs if orb.right > 0]

        for orb in self.gr_orbs: orb.x -= self.game_speed
        self.gr_orbs = [orb for orb in self.gr_orbs if orb.right > 0]

    def check_collisions(self, player_rect, player, space_held=False):
        # 1. Обычные шипы
        for spike in self.obstacles:
            if player_rect.colliderect(spike):
                return "DEATH"

        # 2. Потолочные шипы
        for c_spike in self.ceil_obstacles:
            if player_rect.colliderect(c_spike):
                return "DEATH"

        # Орбы двойного прыжка
        for orb in self.dj_orbs:
            if player_rect.colliderect(orb):
                self.dj_orbs.remove(orb)
                player.has_double_jump = True
                player.can_jump = True
                return "DBL_JMP"

        # Орбы гравитации
        for orb in self.gr_orbs:
            if player_rect.colliderect(orb):
                player.can_jump = True
                if player.used_orb:
                    self.gr_orbs.remove(orb)
                    player.used_orb = False
                return "GRAVITY_CHANGE" 

        # 3. Приземление на платформы и полублоки
        player.on_platform = False 
        
        for plat in self.platforms + self.slabs:
            landing_zone = pygame.Rect(plat.x, plat.y - 8, plat.width, plat.height + 8)
            if player_rect.colliderect(landing_zone):
                if player.vel_y >= 0:
                    if (player_rect.bottom - player.vel_y) <= plat.top + 8:
                        player.y = plat.top - player.size 
                        player.vel_y = 0
                        player.is_jumping = False
                        player.can_jump = True
                        player.on_platform = True
                        
                        if space_held and player.was_in_air and not player.just_landed:
                            player.jump()
                        player.just_landed = True
                        player.was_in_air = False
                        player_rect.y = player.y

        # 4. ИСПРАВЛЕНО: Честный удар боком в стену (учитывает скорость пролета мяча)
        for plat in self.platforms + self.slabs:
            if player_rect.colliderect(plat):
                # Если мяч врезается слева направо (с учетом скорости игры)
                if player_rect.right >= plat.left and player_rect.left < plat.left:
                    # Проверяем, что мяч действительно врезался в стену, а не плавно катится по крыше
                    if player_rect.bottom > plat.top + 6 and player.gravity > 0:
                        return "DEATH"
                    if player_rect.top < plat.bottom - 6 and player.gravity < 0:
                        return "DEATH"
                        
        return "FALSE"

    def draw(self, screen):
        screen.blit(self.bg_image, (self.bg_x1, 0))
        screen.blit(self.bg_image, (self.bg_x2, 0))
        pygame.draw.line(screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2)
        
        for plat in self.platforms:
            pygame.draw.rect(screen, (140, 20, 140), plat)
            pygame.draw.rect(screen, (0, 255, 255), plat, 1)
        
        for slab in self.slabs:
            pygame.draw.rect(screen, (140, 20, 140), slab)
            pygame.draw.rect(screen, (0, 255, 255), slab, 1)
        
        for spike in self.obstacles:
            points = [(spike.left, spike.bottom), (spike.centerx, spike.top), (spike.right, spike.bottom)]
            pygame.draw.polygon(screen, RED, points)
        
        for c_spike in self.ceil_obstacles:
            points = [(c_spike.left, c_spike.top), (c_spike.centerx, c_spike.bottom), (c_spike.right, c_spike.top)]
            pygame.draw.polygon(screen, RED, points)

        for orb in self.dj_orbs:
            screen.blit(self.dj_orb_texture, (orb.x, orb.y))
        for orb in self.gr_orbs:
            screen.blit(self.gr_orb_texture, (orb.x, orb.y))

    def play_music(self):
        pygame.mixer.music.play(-1)
