import pygame
from settings import SCREEN_HEIGHT, CYAN


class Player:
    def __init__(self, lvl, x, floor_y):
        self.size = 40
        self.x = x
        self.floor_y = floor_y
        self.y = floor_y - self.size
        self.game_speed = lvl.lvl_speed

        self.vel_y = 0
        self.gravity = 1
        self.jump_strength = -14
        self.is_jumping = False
        self.can_jump = True
        self.angle = 0
        self.on_platform = False
        self.was_in_air = False  # Флаг для отслеживания приземления
        self.just_landed = False  # Флаг для защиты от дребезга
        self.used_orb = False

        # Загрузка текстуры
        self.texture = pygame.image.load(
            "media/textures/basket_ball.png"
        ).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.size, self.size))

    def jump(self):
        """Прыгает"""
        if self.can_jump:
            self.vel_y = self.jump_strength
            self.is_jumping = True
            self.can_jump = False

    def update(self, space_held=False):
        # Гравитация
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Проверка пола
        if self.y >= self.floor_y - self.size:
            self.y = self.floor_y - self.size
            self.vel_y = 0
            self.is_jumping = False
            self.can_jump = True
            self.on_platform = True

            # Если пробел зажат И мы были в воздухе И не только что приземлились
            if space_held and self.was_in_air and not self.just_landed:
                self.jump()
                self.just_landed = True

            self.was_in_air = False
        else:
            # Мы в воздухе
            # Мы в воздухе
            self.was_in_air = True
            self.just_landed = False
            self.on_platform = False

        if self.gravity < 0 and self.y <= 0:
            self.y = 0
            self.vel_y = 0
            self.is_jumping = False
            self.can_jump = True

            # Автопрыжок от потолка
            if space_held:
                self.jump()

        # Вращение
        if self.gravity > 0:
            if not self.is_jumping:
                self.angle -= self.game_speed * 1.5
            else:
                self.angle -= 5
        if self.gravity < 0:
            if not self.is_jumping:
                self.angle += self.game_speed * 1.5
            else:
                self.angle += 5

    def draw(self, screen):
        rotated_ball = pygame.transform.rotate(self.texture, self.angle)
        rect = rotated_ball.get_rect()
        rect.center = (self.x + self.size // 2, self.y + self.size // 2)
        screen.blit(rotated_ball, rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x + 3, self.y + 3, self.size - 12, self.size - 12)
