import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class LevelOne:
    def __init__(self):
        self.map = []
        #Писать карту надо без пробела в конце и лиших символов, кодировка UTF-8
        with open("media/maps/level1_map.txt", "r", encoding="utf-8") as file:
            for line in file:
                self.map.append(line.strip('\n'))
        
        self.bg_image = pygame.image.load("media/background/level1_bg.jpg").convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.lvl_speed = 7
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.bg_speed = 3  # Скорость движения фона
        self.music_name = "media/music/level1_music.mp3"
    def getMap(self):
        return self.map