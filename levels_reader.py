import pygame
from settings import SCREEN_WIDTH, RED, BLOCK_SIZE
from objects import Object, DoubleJumpOrb, GravityChangeOrb, Platform, Slab

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
        
        START_OFFSET = 0 
        for row_index, row in enumerate(lvl.map):
            for col_index, char in enumerate(row):
                x = START_OFFSET + (col_index * BLOCK_SIZE)
                y = row_index * BLOCK_SIZE
                
                if char == "P":
                    self.platforms.append(Platform(x,y))
                elif char == "X":
                    self.obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "M":
                    self.ceil_obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "S":
                    self.slabs.append(Slab(x,y))
                elif char == "D":
                    self.dj_orbs.append(DoubleJumpOrb(x, y))
                elif char == "G":
                    self.gr_orbs.append(GravityChangeOrb(x, y))

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
        
        # Сдвиг объектов и очистка
        for spike in self.obstacles: spike.x -= self.game_speed
        self.obstacles = [s for s in self.obstacles if s.right > 0]

        for c_spike in self.ceil_obstacles: c_spike.x -= self.game_speed
        self.ceil_obstacles = [s for s in self.ceil_obstacles if s.right > 0]

        for plat in self.platforms: plat.rect.x -= self.game_speed
        self.platforms = [p for p in self.platforms if p.rect.right > 0]

        for slab in self.slabs: slab.rect.x -= self.game_speed
        self.slabs = [s for s in self.slabs if s.rect.right > 0]

        # ИСПРАВЛЕНО: Теперь и двигаем через rect, и проверяем rect.right
        for orb in self.dj_orbs: orb.rect.x -= self.game_speed
        self.dj_orbs = [orb for orb in self.dj_orbs if orb.rect.right > 0]

        for orb in self.gr_orbs: orb.rect.x -= self.game_speed
        self.gr_orbs = [orb for orb in self.gr_orbs if orb.rect.right > 0]

    def check_collisions(self, player_rect, player, space_held=False):
        # Переносим сброс флага платформы на самый верх кадра
        player.on_platform = False 

        # 1. СНАЧАЛА ПРОВЕРЯЕМ СМЕРТЬ (Обычные и потолочные шипы)
        for spike in self.obstacles:
            # Если шипы тоже объекты, пишем spike.rect. Если они остались Rect, то просто spike
            spike_rect = spike.rect if hasattr(spike, 'rect') else spike
            if player_rect.colliderect(spike_rect):
                return spike

        for c_spike in self.ceil_obstacles:
            c_spike_rect = c_spike.rect if hasattr(c_spike, 'rect') else c_spike
            if player_rect.colliderect(c_spike_rect):
                return c_spike

        # 2. ПРОВЕРЯЕМ ОРБЫ
        for orb in self.dj_orbs:
            if player_rect.colliderect(orb.rect):
                return orb

        for orb in self.gr_orbs:
            if player_rect.colliderect(orb.rect):
                return orb

        # 3. ПРИЗЕМЛЕНИЕ НА ПЛАТФОРМЫ И ПОЛУБЛОКИ (Объекты)
        
        # ОБЫЧНАЯ ГРАВИТАЦИЯ (приземляемся сверху на платформу)
        if player.gravity > 0:
            for plat in self.platforms + self.slabs:
                # ИСПРАВЛЕНО: берем координаты из plat.rect
                p_rect = plat.rect 
                
                landing_zone = pygame.Rect(p_rect.x, p_rect.y - 8, p_rect.width, p_rect.height + 8)
                if player_rect.colliderect(landing_zone):
                    if player.vel_y >= 0:
                        if (player_rect.bottom - player.vel_y) <= p_rect.top + 8:
                            player.y = p_rect.top - player.size 
                            player.vel_y = 0
                            player.is_jumping = False
                            player.can_jump = True
                            player.on_platform = True
                            player.was_in_air = False
                            player_rect.y = player.y
                            
                            if space_held:
                                player.jump()
                                player_rect.y = player.y
                                return None

        # ИНВЕРТИРОВАННАЯ ГРАВИТАЦИЯ (приземляемся «снизу» на платформу)
        elif player.gravity < 0:
            for plat in self.platforms + self.slabs:
                p_rect = plat.rect # ИСПРАВЛЕНО: берем plat.rect
                
                landing_zone = pygame.Rect(p_rect.x, p_rect.y, p_rect.width, p_rect.height + 8)
                if player_rect.colliderect(landing_zone):
                    if player.vel_y <= 0:  
                        if (player_rect.top - player.vel_y) >= p_rect.bottom - 8:
                            player.y = p_rect.bottom  
                            player.vel_y = 0
                            player.is_jumping = False
                            player.can_jump = True
                            player.on_platform = True
                            player.was_in_air = False
                            player_rect.y = player.y
                            
                            if space_held:
                                player.jump()
                                player_rect.y = player.y
                                return None

        # 4. УДАР БОКОМ В СТЕНУ (Фронтальное столкновение)
        if not player.on_platform:
            for plat in self.platforms + self.slabs:
                p_rect = plat.rect # ИСПРАВЛЕНО: берем plat.rect
                
                if player_rect.colliderect(p_rect):
                    # Если мяч врезается слева направо
                    if player_rect.right >= p_rect.left and player_rect.left < p_rect.left:
                        if player.gravity > 0 and player_rect.bottom > p_rect.top + 10:
                            return plat
                        if player.gravity < 0 and player_rect.top < p_rect.bottom - 10:
                            return plat
                        
        return None

    def draw(self, screen):
        screen.blit(self.bg_image, (self.bg_x1, 0))
        screen.blit(self.bg_image, (self.bg_x2, 0))
        pygame.draw.line(screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2)
        
        for plat in self.platforms:
            plat.draw(screen)
        
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
            orb.draw(screen)
        for orb in self.gr_orbs:
             orb.draw(screen)

    def play_music(self):
        pygame.mixer.music.play(-1)
