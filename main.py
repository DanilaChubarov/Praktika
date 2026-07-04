import pygame
import sys
from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    BLACK,
    FPS,
)
from player import Player
from levels_reader import LevelReader
from level1 import LevelOne

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Python Geometry Dash Clone")
clock = pygame.time.Clock()

# Переменные мира
floor_y = SCREEN_HEIGHT - 60
FINISH_LINE = 30000  # Координата финиша (увеличил)

def draw_menu():
    """Отрисовка меню"""
    screen.fill(BLACK)
    font_title = pygame.font.SysFont(None, 72)
    font_text = pygame.font.SysFont(None, 36)
    
    title = font_title.render("GEOMETRY DASH", True, WHITE)
    start_text = font_text.render("SPACE - Начать / Перезапустить", True, WHITE)
    hint = font_text.render("Зажимай SPACE чтобы прыгать непрерывно!", True, WHITE)
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 250))
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 320))
    
    pygame.display.flip()

def draw_game_over(final_score):
    """Отрисовка экрана проигрыша"""
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    game_over_text = font.render("GAME OVER!", True, (255, 50, 50))
    score_text = font_small.render(f"Счет: {final_score}", True, WHITE)
    restart_text = font_small.render("SPACE - Начать заново", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
    
    pygame.display.flip()

def draw_victory(final_score):
    """Отрисовка экрана победы"""
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    victory_text = font.render("ПОБЕДА!", True, (50, 255, 50))
    score_text = font_small.render(f"Финальный счет: {final_score}", True, WHITE)
    restart_text = font_small.render("SPACE - Играть снова", True, WHITE)
    
    screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
    
    pygame.display.flip()

def reset_game():
    """Сброс игры"""
    curr_lvl = LevelOne()
    player = Player(curr_lvl, x=100, floor_y=floor_y)
    level = LevelReader(curr_lvl, floor_y=floor_y)
    
    return player, level, curr_lvl

# Инициализация игры
player, level, curr_lvl = reset_game()
game_state = "menu"  # "menu", "playing", "game_over", "victory"
space_pressed = False

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)
    
    if game_state == "menu":
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "playing"
                level.play_music()
                space_pressed = False
                
    elif game_state == "playing":
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # НАЖАТИЕ кнопки Space
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True
                player.jump()
            
            # ОТПУСКАНИЕ кнопки Space
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_pressed = False
            
            # Клик мыши (альтернатива)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.jump()
        
        # Физика и обновление
        player.update(space_held=space_pressed)
        level.update()
        
        # Проверка коллизий
        player_rect = player.get_rect()
        if level.check_collisions(player_rect, player, space_held=space_pressed):
            game_state = "game_over"
        
        # Проверка победы (достижение финиша)
        if level.world_offset >= FINISH_LINE:
            game_state = "victory"
        
        # Отрисовка игры
        level.draw(screen)
        player.draw(screen)
        
        # Отображение UI
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Счет: {level.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        
    elif game_state == "game_over":
        draw_game_over(level.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player, level, lvl = reset_game()
                game_state = "menu"
                space_pressed = False
                
    elif game_state == "victory":
        draw_victory(level.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player, level, lvl = reset_game()
                game_state = "menu"
                space_pressed = False

pygame.quit()
sys.exit()
