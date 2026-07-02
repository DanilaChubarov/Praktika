import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
class LevelOne:
    def __init__(self):
        self.map = [
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", # Потолок
            "   M        M          M                 M       MMMMM             ", # Шипы на потолке
            "                                                                   ",
            "                                                                   ",
            "                     PPPPPP          PPPPPP                        ", # Верхний ярус платформ
            "                       XX              XX                          ", # Шипы НА платформах
            "                                                                   ",
            "               PPPP                                                ", # Нижний ярус платформ
            "                XX                                                 ",
            "          PPP                                                      ",
            "    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   "  # Шипы на основном полу
        ]
        self.bg_image = pygame.image.load("41524.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def getMap():
        return map    