import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class LevelOne:
    def __init__(self):
        self.map = [
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",  # Потолок
            "   M        M          M                 M       MMMMM             ",  # Шипы на потолке
            "                                                                   ",
            "                                                                   ",
            "                       PPPPPP        PPPPPP                        ",  # Верхний ярус платформ
            "                         MM            MM                          ",  # Шипы НА платформах
            "                                                                   ",
            "               PPPP                                                ",  # Нижний ярус платформ
            "                MM                                                 ",
            "          PPP                                                      ",
            "    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   ",  # Шипы на основном полу
        ]
        
        self.bg_image = pygame.image.load("media/background/level1_bg.jpg").convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.bg_speed = 5  # Скорость движения фона
        self.music_name = "media/music/level1_music.mp3"
    def getMap(self):
        return self.map