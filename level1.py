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
        # ===== ФОН С ДВИЖЕНИЕМ =====
        self.bg_image = pygame.image.load("41524.jpg").convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.game_speed = 7  # Скорость движения фона

    def update(self):
        self.bg_x1 -= self.game_speed
        self.bg_x2 -= self.game_speed

        # Зацикливание фона
        if self.bg_x1 <= -SCREEN_WIDTH:
            self.bg_x1 = self.bg_x2 + SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH:
            self.bg_x2 = self.bg_x1 + SCREEN_WIDTH

    def draw_background(self, screen):
        screen.blit(self.bg_image, (self.bg_x1, 0))
        screen.blit(self.bg_image, (self.bg_x2, 0))

    def getMap(self):
        return self.map
