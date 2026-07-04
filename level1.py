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
<<<<<<< HEAD
        # ===== ФОН С ДВИЖЕНИЕМ =====
        self.bg_image = pygame.image.load("media/background/level1_bg.jpg").convert()
=======
        
        self.bg_image = pygame.image.load("41524.jpg").convert()
>>>>>>> dfa31749d4cc0dcfddfa001dc2952466f254ae75
        self.bg_image = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.music = pygame
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
<<<<<<< HEAD
        self.game_speed = 7  # Скорость движения фона

    def update(self):
        self.bg_x1 -= self.game_speed
        self.bg_x2 -= self.game_speed

        # Зацикливание фона
        if self.bg_x1 <= -SCREEN_WIDTH:
            self.bg_x1 = self.bg_x2 + SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH:
            self.bg_x2 = self.bg_x1 + SCREEN_WIDTH
=======
        self.bg_speed = 10  # Скорость движения фона
>>>>>>> dfa31749d4cc0dcfddfa001dc2952466f254ae75

    def getMap(self):
        return self.map
