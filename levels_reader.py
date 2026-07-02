import pygame
import random
from settings import SCREEN_WIDTH, RED

class LevelReader:
    def __init__(self, lvl, floor_y):
        self.floor_y = floor_y
        # Уровень сам хранит и контролирует свои препятствия
        self.obstacles = [SCREEN_WIDTH, SCREEN_WIDTH + 400]
        self.score = 0
        self.obstacles = []  # Изначально список пустой, заполним его из карты
        
        # Настройки из переданного класса уровня
        self.bg_image = pygame.transform.scale(lvl.bg_image, (SCREEN_WIDTH, self.floor_y + 50))
        
        # Читаем текстовую карту
        BLOCK_SIZE = 40      # Ширина одного шипа
        START_OFFSET = 600   # Отступ от игрока на старте (чтобы успеть среагировать)
        
        for index, char in enumerate(lvl.map):
            if char == "X":
                # Рассчитываем точную X-координату для каждого шипа
                x_position = START_OFFSET + (index * BLOCK_SIZE)
                self.obstacles.append(x_position)

    def update(self, game_speed):
        """Двигает шипы влево и спавнит новые"""
        new_obstacles = []
        for obs_x in self.obstacles:
            obs_x -= game_speed
            if obs_x > -40:
                new_obstacles.append(obs_x)
            else:
                self.score += 1
                
        self.obstacles = new_obstacles

    def check_collisions(self, player_rect):
        """Проверяет столкновение игрока с любым шипом на уровне"""
        for obs_x in self.obstacles:
            spike_rect = pygame.Rect(obs_x, self.floor_y - 40, 40, 40)
            if player_rect.colliderect(spike_rect):
                return True
        return False

    def draw(self, screen):
        """Рисует пол и шипы текущего уровня"""
        # Линия пола
        pygame.draw.line(screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2)
        # Все активные шипы
        for obs_x in self.obstacles:
            points = [(obs_x, self.floor_y), (obs_x + 20, self.floor_y - 40), (obs_x + 40, self.floor_y)]
            pygame.draw.polygon(screen, RED, points)
