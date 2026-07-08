import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class BaseLevel:
    def __init__(self, level_num, lvl_speed, bg_speed):
        self.map = []

        # Автоматическое чтение нужной карты
        map_path = f"media/maps/level{level_num}_map.txt"
        with open(map_path, "r", encoding="utf-8") as file:
            for line in file:
                self.map.append(line.strip("\n"))

        # Автоматическая загрузка фона
        bg_path = f"media/background/level{level_num}_bg.jpg"
        self.bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # Настройки движения и музыки
        self.lvl_speed = lvl_speed
        self.bg_speed = bg_speed
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.music_name = f"media/music/level{level_num}_music.mp3"

    def getMap(self):
        return self.map
