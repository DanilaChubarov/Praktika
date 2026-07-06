import pygame
from levels_reader import BLOCK_SIZE
class Object:
    def update_list(obj, list, game_speed):
        obj.x -= game_speed
        list = [obj for obj in list if obj.right > 0]
        return list
class DoubleJumpOrb(Object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

    