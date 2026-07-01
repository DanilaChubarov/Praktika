import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 50, 50)

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Geometry Dash Clone")
bg_image = pygame.image.load("41524.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
clock = pygame.time.Clock()

# Параметры игрока
player_size = 40
player_x = 100
player_y = SCREEN_HEIGHT - player_size - 50  # 50px - высота пола
player_vel_y = 0
gravity = 1
jump_strength = -16
is_jumping = False
ball_angle = 0

#загрузка текстур
bg_image = pygame.image.load("41524.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
ball_texture = pygame.image.load("basket_ball.png").convert_alpha()
ball_texture = pygame.transform.scale(ball_texture, (player_size, player_size))

# Параметры игрового мира
floor_y = SCREEN_HEIGHT - 50
game_speed = 7
score = 0

# Препятствия (список x-координат)
obstacles = [800, 1200]

def draw_spike(x, y):
    """Рисует треугольный шип"""
    points = [(x, y), (x + 20, y - 40), (x + 40, y)]
    pygame.draw.polygon(screen, RED, points)

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)
    screen.blit(bg_image, (0,0))

    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = jump_strength
                is_jumping = True

    # 2. Физика игрока (гравитация)
    player_vel_y += gravity
    player_y += player_vel_y
    if not is_jumping:
        ball_angle -= game_speed * 1.5  # Минус, чтобы крутился вперед (по часовой стрелке)
    else:
        ball_angle -= 5  # Скорость вращения в воздухе

    # Проверка столкновения с полом
    if player_y >= floor_y - player_size:
        player_y = floor_y - player_size
        player_vel_y = 0
        is_jumping = False

    # 3. Движение и логика препятствий
    new_obstacles = []
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    player_circle_center = (player_rect.centerx, player_rect.centery)
    player_circle_radius = (player_size//2)

    for obs_x in obstacles:
        obs_x -= game_speed  # Сдвиг препятствия влево
        
        # Создаем хитбокс шипа для проверки коллизий
        spike_rect = pygame.Rect(obs_x, floor_y - 40, 40, 40)
        
        # Проверка на проигрыш
        if player_rect.colliderect(spike_rect):
            print(f"Final Score: {score}")
            running = False  # Игра окончена при столкновении

        # Если шип улетел за экран, увеличиваем счет
        if obs_x > -40:
            new_obstacles.append(obs_x)
        else:
            score += 1
            # Спавним новый шип за экраном с рандомным отступом
            new_obstacles.append(SCREEN_WIDTH + random.randint(200, 500))

    obstacles = new_obstacles

    # 4. Отрисовка графики
    # Пол
    pygame.draw.line(screen, WHITE, (0, floor_y), (SCREEN_WIDTH, floor_y), 2)
    # Игрок (Куб)
    # 1. Поворачиваем исходную текстуру на текущий угол
    rotated_ball = pygame.transform.rotate(ball_texture, ball_angle)

    # 2. Берем прямоугольник повернутой картинки
    ball_rect = rotated_ball.get_rect()

    # 3. Центрируем этот прямоугольник ровно по текущим координатам игрока
    ball_rect.center = (player_x + player_size // 2, player_y + player_size // 2)

    # 4. Рисуем повернутый шар на экране
    screen.blit(rotated_ball, ball_rect.topleft)
    # Препятствия
    for obs_x in obstacles:
        draw_spike(obs_x, floor_y)

    # Отображение счета
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
