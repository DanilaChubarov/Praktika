import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
class LevelOne:
    def __init__(self):
        self.map = "      XX        XX          XX      X     X    X   XXXXXX   X"
        self.bg_image = pygame.image.load("41524.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def getMap():
        return map    