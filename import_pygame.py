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
LIGHT_GRAY = (200, 200, 200)

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Geometry Dash Clone")
clock = pygame.time.Clock()

# Параметры игрока
player_size = 40
player_x = 100
player_y = SCREEN_HEIGHT - player_size - 50
player_vel_y = 0
gravity = 1
jump_strength = -16
is_jumping = False
ball_angle = 0

# Загрузка текстур
bg_image = pygame.image.load("41524.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
ball_texture = pygame.image.load("basket_ball.png").convert_alpha()
ball_texture = pygame.transform.scale(ball_texture, (player_size, player_size))
ground_texture = pygame.image.load("ground.png").convert_alpha()
ground_texture = pygame.transform.scale(ground_texture, (SCREEN_WIDTH, 50))
bg_x1 = 0
bg_x2 = SCREEN_WIDTH
ground_x1 = 0
ground_x2 = SCREEN_WIDTH

# Параметры игрового мира
floor_y = SCREEN_HEIGHT - 70
game_speed = 7
score = 0

# Препятствия
obstacles = [800, 1200]
floor_offset = 0
floor_line_height = 15
floor_line_spacing = 40


def draw_spike(x, y):
    """Рисует треугольный шип"""
    points = [(x, y), (x + 20, y - 40), (x + 40, y)]
    pygame.draw.polygon(screen, RED, points)


# Главный цикл игры
running = True
while running:
    clock.tick(FPS)

    # ФОН
    bg_x1 -= game_speed
    bg_x2 -= game_speed
    if bg_x1 <= -SCREEN_WIDTH:
        bg_x1 = bg_x2 + SCREEN_WIDTH
    if bg_x2 <= -SCREEN_WIDTH:
        bg_x2 = bg_x1 + SCREEN_WIDTH

    # Рисуем фон в КАЖДОМ кадре (это было вне цикла!)
    screen.blit(bg_image, (bg_x1, 0))
    screen.blit(bg_image, (bg_x2, 0))

    ground_x1 -= game_speed
    ground_x2 -= game_speed
    if ground_x1 <= -SCREEN_WIDTH:
        ground_x1 = ground_x2 + SCREEN_WIDTH
    if ground_x2 <= -SCREEN_WIDTH:
        ground_x2 = ground_x1 + SCREEN_WIDTH

    screen.blit(ground_texture, (ground_x1, floor_y))
    screen.blit(ground_texture, (ground_x2, floor_y))

    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = jump_strength
                is_jumping = True

    # 2. Физика игрока
    player_vel_y += gravity
    player_y += player_vel_y
    if not is_jumping:
        ball_angle -= game_speed * 1.5
    else:
        ball_angle -= 5

    if player_y >= floor_y - player_size:
        player_y = floor_y - player_size
        player_vel_y = 0
        is_jumping = False

    # 3. Движение препятствий
    new_obstacles = []
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    for obs_x in obstacles:
        obs_x -= game_speed

        spike_rect = pygame.Rect(obs_x, floor_y - 40, 40, 40)

        if player_rect.colliderect(spike_rect):
            print(f"Final Score: {score}")
            running = False

        if obs_x > -40:
            new_obstacles.append(obs_x)
        else:
            score += 1
            new_obstacles.append(SCREEN_WIDTH + random.randint(200, 500))

    obstacles = new_obstacles

    # 4. Отрисовка

    # Игрок
    rotated_ball = pygame.transform.rotate(ball_texture, ball_angle)
    ball_rect = rotated_ball.get_rect()
    ball_rect.center = (player_x + player_size // 2, player_y + player_size // 2)
    screen.blit(rotated_ball, ball_rect.topleft)

    # Препятствия
    for obs_x in obstacles:
        draw_spike(obs_x, floor_y)

    # Счет
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
