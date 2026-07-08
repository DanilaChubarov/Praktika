import pygame
from settings import SCREEN_WIDTH, RED, BLOCK_SIZE
from objects import (
    Object,
    DoubleJumpOrb,
    GravityChangeOrb,
    Platform,
    Slab,
    Spike,
    CeilingSpike,
    ShipPortal,
    CubePortal
)
from enum import Enum, auto


class LevelReader:
    def __init__(self, lvl, floor_y):
        self.lvl = lvl
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
        self.sh_ports = []
        self.c_ports = []
        self.game_mode = GameState.CUBE

        self.bg_image = pygame.transform.scale(
            lvl.bg_image, (SCREEN_WIDTH, self.floor_y + 50)
        )
        self.bg_x1 = lvl.bg_x1
        self.bg_x2 = lvl.bg_x2
        self.bg_speed = lvl.bg_speed
        # Загружаем музыку
        try:
            pygame.mixer.music.load(lvl.music_name)
        except:
            pass

        START_OFFSET = 0

        pygame.mixer.music.load(lvl.music_name)

        BLOCK_SIZE = 40
        START_OFFSET = 0
      
        
        for row_index, row in enumerate(lvl.map):
            for col_index, char in enumerate(row):
                x = START_OFFSET + (col_index * BLOCK_SIZE)
                y = row_index * BLOCK_SIZE

                if char == "P":
                    self.platforms.append(Platform(x, y))
                elif char == "X":
                    self.obstacles.append(Spike(x, y))
                elif char == "M":
                    self.ceil_obstacles.append(CeilingSpike(x, y))
                elif char == "S":
                    self.slabs.append(Slab(x, y))
                elif char == "D":
                    self.dj_orbs.append(DoubleJumpOrb(x, y))
                elif char == "G":
                    self.gr_orbs.append(GravityChangeOrb(x, y))
                elif char == "H":
                    self.sh_ports.append(ShipPortal(x, y))
                elif char == "C":
                    self.c_ports.append(CubePortal(x, y))

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

        # Все объекты двигаем и фильтруем через .rect — единообразно
        for spike in self.obstacles:
            spike.rect.x -= self.game_speed
        self.obstacles = [s for s in self.obstacles if s.rect.right > 0]

        for c_spike in self.ceil_obstacles:
            c_spike.rect.x -= self.game_speed
        self.ceil_obstacles = [s for s in self.ceil_obstacles if s.rect.right > 0]

        for plat in self.platforms:
            plat.rect.x -= self.game_speed
        self.platforms = [p for p in self.platforms if p.rect.right > 0]

        for slab in self.slabs:
            slab.rect.x -= self.game_speed
        self.slabs = [s for s in self.slabs if s.rect.right > 0]

        for orb in self.dj_orbs:
            orb.rect.x -= self.game_speed
        self.dj_orbs = [orb for orb in self.dj_orbs if orb.rect.right > 0]

        for orb in self.gr_orbs:
            orb.rect.x -= self.game_speed
        self.gr_orbs = [orb for orb in self.gr_orbs if orb.rect.right > 0]
        for port in self.sh_ports:
            port.rect.x -= self.game_speed
        self.sh_ports = [port for port in self.sh_ports if port.rect.right > 0]
        for port in self.c_ports:
            port.rect.x -= self.game_speed
        self.c_ports = [port for port in self.c_ports if port.rect.right > 0]

    def check_collisions(self, player_rect, player, space_held=False):
        # ВАЖНО: сбрасываем флаг платформы в начале каждого кадра,
        # иначе проверка удара об стену (пункт 4) перестанет работать
        # после первого приземления.
        player.on_platform = False

        # 1. Обычные и потолочные шипы — смерть
        for spike in self.obstacles:
            if player_rect.colliderect(spike.rect):
                return spike

        for c_spike in self.ceil_obstacles:
            if player_rect.colliderect(c_spike.rect):
                return c_spike

        # 2. ПРОВЕРЯЕМ ОРБЫ
        for orb in self.dj_orbs:
            if player_rect.colliderect(orb.rect):
                return orb

        for orb in self.gr_orbs:
            if player_rect.colliderect(orb.rect):
                return orb
        for port in self.sh_ports:
            if player_rect.colliderect(port.rect):
                return port
        for port in self.c_ports:
            if player_rect.colliderect(port.rect):
                return port
              
        # 3. ПРИЗЕМЛЕНИЕ НА ПЛАТФОРМЫ И ПОЛУБЛОКИ
        if player.gravity > 0:
            
            player.on_platform = False
            
            for plat in self.platforms + self.slabs:
                p_rect = plat.rect
                landing_zone = pygame.Rect(
                    p_rect.x, p_rect.y - 8, p_rect.width, p_rect.height + 8
                )
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
                if player.y >= player.floor_y - player.size:
                    player.is_jumping = False
                    player.can_jump = True
                    player.on_platform = True
            if not player.on_platform:
                player.can_jump = False
        elif player.gravity < 0:
            for plat in self.platforms + self.slabs:
                p_rect = plat.rect
                landing_zone = pygame.Rect(
                    p_rect.x, p_rect.y, p_rect.width, p_rect.height + 8
                )
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

        # 4. УДАР БОКОМ В СТЕНУ
        if not player.on_platform or  (player.y >= player.floor_y - player.size):
            for plat in self.platforms + self.slabs:
                p_rect = plat.rect
                if player_rect.colliderect(p_rect):
                    if (
                        player_rect.right >= p_rect.left
                        and player_rect.left < p_rect.left
                    ):
                        if player.gravity > 0 and player_rect.bottom > p_rect.top + 10:
                            return plat
                        if player.gravity < 0 and player_rect.top < p_rect.bottom - 10:
                            return plat

        return None

    def draw(self, screen):
        screen.blit(self.bg_image, (self.bg_x1, 0))
        screen.blit(self.bg_image, (self.bg_x2, 0))
        pygame.draw.line(
            screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2
        )

        for plat in self.platforms:
            plat.draw(screen)

        for slab in self.slabs:
            slab.draw(screen)

        for spike in self.obstacles:
            spike.draw(screen)

        for c_spike in self.ceil_obstacles:
           c_spike.draw(screen)
    
        for orb in self.dj_orbs:
            orb.draw(screen)
        for orb in self.gr_orbs:
            orb.draw(screen)
        for port in self.sh_ports:
            port.draw(screen)
        for port in self.c_ports:
            port.draw(screen)

    def play_music(self):
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
class GameState(Enum):
    CUBE = auto()       
    SHIP = auto()       
    WAVE = auto()