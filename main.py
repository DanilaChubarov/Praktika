import pygame
import sys
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, FPS  # Всё нужное импортируем из настроек
from player import Player
from levels_reader import LevelReader
from level1 import LevelOne
   
# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Geometry Dash Clone")
clock = pygame.time.Clock()
lvl = LevelOne()

# Переменные мира
floor_y = SCREEN_HEIGHT - 50
game_speed = 10

# Создаем объекты персонажа и менеджера уровней
player = Player(x=100, floor_y=floor_y)
level = LevelReader(lvl,  floor_y=floor_y)  # Класс сам создаст шипы внутри себя!

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)
    screen.blit(lvl.bg_image, (0, 0))  # Очищаем экран фоном

    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        is_space_pressed = (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
        is_mouse_clicked = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
        
        if is_mouse_clicked or is_space_pressed:
            player.jump()  # Безопасно вызываем метод прыжка из класса Player

    # 2. Физика и обновление позиций
    player.update(game_speed)
    level.update(game_speed)  # Уровень сам двигает свои шипы
 
    # 3. Проверка коллизий через класс уровня
    player_rect = player.get_rect()
    if level.check_collisions(player_rect, player, game_speed):
        print(f"Game Over! Final Score: {level.score}")
        running = False  # Столкнулись с шипом -> проиграли
                        
    # 4. Отрисовка графики
    level.draw(screen)   # Сначала рисуем пол и шипы уровня
    player.draw(screen)  # Поверх рисуем крутящийся шарик
       
    # Отображение счета (берем его из объекта уровня)
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {level.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
