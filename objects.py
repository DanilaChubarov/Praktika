import pygame
from levels_reader import BLOCK_SIZE


class Object:
    def __init__(self, x, y, width, height):
        self.size = BLOCK_SIZE
        self.rect = pygame.Rect(x, y, width, height)
        self.x = self.rect.x
        self.y = self.rect.y
        self.right = self.x + width
        self.type = None

    def update_list(self, list, game_speed):
        self.x -= game_speed
        list = [self for self in list if self.right > 0]
        return list


class DoubleJumpOrb(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE+10, height=BLOCK_SIZE+10)
        self.type = "DBL_JMP"
        self.texture = pygame.image.load(
            "media/textures/double_jump.png"
        ).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (BLOCK_SIZE, BLOCK_SIZE))

    def draw(self, screen):
        screen.blit(self.texture, (self.rect.x, self.rect.y))


class GravityChangeOrb(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE+10, height=BLOCK_SIZE+10)
        self.type = "GRAVITY_CHANGE"
        self.texture = pygame.image.load(
            "media/textures/gravity_orb.png"
        ).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (BLOCK_SIZE, BLOCK_SIZE))

    def draw(self, screen):
        screen.blit(self.texture, (self.rect.x, self.rect.y))


class Platform(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE, height=BLOCK_SIZE)
        self.type = "DEATH"

    def draw(self, screen):
        pygame.draw.rect(screen, (140, 20, 140), self.rect)
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 1)


class Slab(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE, height=BLOCK_SIZE // 2)
        self.type = "DEATH"


class Spike(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE, height=BLOCK_SIZE)
        self.type = "DEATH"


class CeilingSpike(Object):
    def __init__(self, x, y):
        super().__init__(x, y, width=BLOCK_SIZE, height=BLOCK_SIZE)
        self.type = "DEATH"
