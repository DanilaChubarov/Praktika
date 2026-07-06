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

# Импортируем уровни из новых файлов (по нашей новой структуре)
from levels.level1 import LevelOne
from levels.level2 import LevelTwo
from levels.level3 import LevelThree

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Python Geometry Dash Clone")
clock = pygame.time.Clock()

# Переменные мира
floor_y = SCREEN_HEIGHT - 60
FINISH_LINE = 30000  # Координата финиша

def draw_menu():
    screen.fill(BLACK)
    title = pygame.font.SysFont(None, 72).render("GEOMETRY DASH", True, WHITE)
    f = pygame.font.SysFont(None, 40)

    t1 = f.render("1 - Level 1 (Easy)", True, WHITE)
    t2 = f.render("2 - Level 2 (Medium)", True, WHITE)
    t3 = f.render("3 - Level 3 (Hard)", True, WHITE)
    t4 = f.render("ESC - Exit", True, WHITE)

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(t1, (340, 200))
    screen.blit(t2, (340, 250))
    screen.blit(t3, (340, 300))
    screen.blit(t4, (340, 380))
    pygame.display.flip()

def draw_game_over(final_score):
    screen.fill(BLACK) # Очищаем экран перед текстом
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    game_over_text = font.render("GAME OVER!", True, (255, 50, 50))
    score_text = font_small.render(f"Счет: {final_score}", True, WHITE)
    restart_text = font_small.render("SPACE - В главное меню", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
    pygame.display.flip()

def draw_victory(final_score):
    screen.fill(BLACK) # Очищаем экран перед текстом
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    victory_text = font.render("ПОБЕДА!", True, (50, 255, 50))
    score_text = font_small.render(f"Финальный счет: {final_score}", True, WHITE)
    restart_text = font_small.render("SPACE - В главное меню", True, WHITE)
    
    screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
    pygame.display.flip()

def reset_game(level_class):
    curr_lvl = level_class()
    player = Player(curr_lvl, x=100, floor_y=floor_y)
    level = LevelReader(curr_lvl, floor_y=floor_y)
    return player, level, curr_lvl

# Первоначальная инициализация игры
selected_level = LevelOne
player, level, curr_lvl = reset_game(selected_level)
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
            
            # ИСПРАВЛЕНО: Кнопки выбора уровней теперь внутри цикла событий меню!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = LevelOne
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                elif event.key == pygame.K_2:
                    selected_level = LevelTwo
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                elif event.key == pygame.K_3:
                    selected_level = LevelThree
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                
    elif game_state == "playing":
        just_pressed = False
        # Обработка событий игрового процесса
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True
                just_pressed = True
                player.jump()
            
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_pressed = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                just_pressed = True
                player.jump()
        
        # Физика и обновление 
        level.update()
        player.update(space_held=space_pressed)
        
        
        # ИСПРАВЛЕНО: Вызываем проверку один раз и сохраняем результат в переменную
        player_rect = player.get_rect()
        hit_object = level.check_collisions(player_rect, player)
         
            
        if hit_object is not None:  # Игрок столкнулся с каким-то орбом
            if hit_object.type == "DEATH":
                game_state = "game_over"
                pygame.mixer.music.stop() # Останавливаем музыку при смерти
            
            if hit_object.type == "DEATH":
                game_state = "game_over"
            if just_pressed:          # Игрок нажал прыжок именно в этот кадр
                
                # Проверяем ТИП орба и выполняем нужное действие
                if hit_object.type == "DBL_JMP":
                    level.dj_orbs.remove(hit_object)
                    player.vel_y = 0 # Удаляем из списка желтых
                    player.can_jump = True
                    player.jump()
                    just_pressed = False
                    
                elif hit_object.type == "GRAVITY_CHANGE":
                    level.gr_orbs.remove(hit_object) # ...или из списка розовых
                    player.gravity *= -1
                    player.jump_strength *= -1
                    player.jump()
                                            
        # Проверка победы (достижение финиша)
        if level.world_offset >= FINISH_LINE:
            game_state = "victory"
            pygame.mixer.music.stop()
        
        # Отрисовка игры          
        level.draw(screen)
        player.draw(screen)
        
        # Отображение UI (Счет)
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
                # ИСПРАВЛЕНО: Теперь сбрасывается корректно с передачей выбранного уровня
                player, level, curr_lvl = reset_game(selected_level)
                game_state = "menu"
                space_pressed = False
                
    elif game_state == "victory":
        draw_victory(level.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # ИСПРАВЛЕНО: Сброс для экрана победы
                player, level, curr_lvl = reset_game(selected_level)
                game_state = "menu"
                space_pressed = False

pygame.quit()
sys.exit()
