import pygame
from settings import SCREEN_HEIGHT, CYAN

class Player:
    def __init__(self, x, floor_y):
        self.size = 40
        self.x = x
        self.floor_y = floor_y
        self.y = floor_y - self.size
        
        self.vel_y = 0
        self.gravity = 1
        self.jump_strength = -16
        self.is_jumping = False
        self.angle = 0
        
        # Загрузка текстуры
        self.texture = pygame.image.load("basket_ball.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.size, self.size))

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_strength
            self.is_jumping = True

    def update(self, game_speed):
        # Гравитация
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Проверка пола
        if self.y >= self.floor_y - self.size:
            self.y = self.floor_y - self.size
            self.vel_y = 0
            self.is_jumping = False

        # Вращение
        if not self.is_jumping:
            self.angle -= game_speed * 1.5
        else:
            self.angle -= 5

    def draw(self, screen):
        rotated_ball = pygame.transform.rotate(self.texture, self.angle)
        rect = rotated_ball.get_rect()
        rect.center = (self.x + self.size // 2, self.y + self.size // 2)
        screen.blit(rotated_ball, rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x + 6 , self.y+6, self.size-12, self.size-12)
