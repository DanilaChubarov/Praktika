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

# Импортируем уровни
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
FINISH_LINE = 30000

# Загружаем фоновую картинку для меню (такая же, как в игре)
menu_bg = pygame.image.load("media/background/level1_bg.jpg").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

btn_width = 220
btn_height = 180
spacing = 70
total_width = btn_width * 3 + spacing * 2
start_x = (SCREEN_WIDTH - total_width) // 2 - 30

# Кнопки уровней (прямоугольники)
LEVEL1_BTN = pygame.Rect(start_x, 160, btn_width, btn_height)
LEVEL2_BTN = pygame.Rect(start_x + btn_width + spacing, 160, btn_width, btn_height)
LEVEL3_BTN = pygame.Rect(
    start_x + (btn_width + spacing) * 2, 160, btn_width, btn_height
)


def draw_menu():
    """Отрисовка меню с тремя кнопками и фоном"""
    # Рисуем фон (как в игре)
    screen.blit(menu_bg, (0, 0))

    # Затемнение фона для читаемости текста
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)  # полупрозрачный
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font_title = pygame.font.SysFont(None, 64)
    font_level = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)

    # Заголовок
    title = font_title.render("GEOMETRY DASH", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

    # ---------- КНОПКА LEVEL 1 ----------
    color1 = (70, 160, 70)
    pygame.draw.rect(screen, color1, LEVEL1_BTN, border_radius=15)
    pygame.draw.rect(screen, WHITE, LEVEL1_BTN, 2, border_radius=15)

    text = font_level.render("LEVEL 1", True, WHITE)
    screen.blit(text, (LEVEL1_BTN.centerx - text.get_width() // 2, LEVEL1_BTN.y + 50))

    sub = font_small.render("EASY", True, (200, 255, 200))
    screen.blit(sub, (LEVEL1_BTN.centerx - sub.get_width() // 2, LEVEL1_BTN.y + 100))

    play = font_small.render("▶ PLAY", True, WHITE)
    screen.blit(play, (LEVEL1_BTN.centerx - play.get_width() // 2, LEVEL1_BTN.y + 150))

    # ---------- КНОПКА LEVEL 2 ----------
    color2 = (180, 160, 70)
    pygame.draw.rect(screen, color2, LEVEL2_BTN, border_radius=15)
    pygame.draw.rect(screen, WHITE, LEVEL2_BTN, 2, border_radius=15)

    text = font_level.render("LEVEL 2", True, WHITE)
    screen.blit(text, (LEVEL2_BTN.centerx - text.get_width() // 2, LEVEL2_BTN.y + 50))

    sub = font_small.render("MEDIUM", True, (255, 255, 200))
    screen.blit(sub, (LEVEL2_BTN.centerx - sub.get_width() // 2, LEVEL2_BTN.y + 100))

    play = font_small.render("▶ PLAY", True, WHITE)
    screen.blit(play, (LEVEL2_BTN.centerx - play.get_width() // 2, LEVEL2_BTN.y + 150))

    # ---------- КНОПКА LEVEL 3 ----------
    color3 = (160, 70, 70)
    pygame.draw.rect(screen, color3, LEVEL3_BTN, border_radius=15)
    pygame.draw.rect(screen, WHITE, LEVEL3_BTN, 2, border_radius=15)

    text = font_level.render("LEVEL 3", True, WHITE)
    screen.blit(text, (LEVEL3_BTN.centerx - text.get_width() // 2, LEVEL3_BTN.y + 50))

    sub = font_small.render("HARD", True, (255, 200, 200))
    screen.blit(sub, (LEVEL3_BTN.centerx - sub.get_width() // 2, LEVEL3_BTN.y + 100))

    play = font_small.render("▶ PLAY", True, WHITE)
    screen.blit(play, (LEVEL3_BTN.centerx - play.get_width() // 2, LEVEL3_BTN.y + 150))

    # Подсказка внизу
    # hint = font_small.render("Нажми на кнопку мышкой", True, WHITE)
    # screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))

    pygame.display.flip()


def draw_game_over(final_score):
    """Отрисовка экрана проигрыша"""
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    game_over_text = font.render("GAME OVER!", True, (255, 50, 50))
    score_text = font_small.render(f"Счет: {final_score}", True, WHITE)
    restart_text = font_small.render("SPACE - В главное меню", True, WHITE)

    screen.blit(
        game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150)
    )
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
    pygame.display.flip()


def draw_victory(final_score):
    """Отрисовка экрана победы"""
    screen.fill(BLACK)
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
    """Сброс игры для выбранного уровня"""
    curr_lvl = level_class()
    player = Player(curr_lvl, x=100, floor_y=floor_y)
    level = LevelReader(curr_lvl, floor_y=floor_y)
    return player, level, curr_lvl


# Инициализация
selected_level = LevelOne
player, level, curr_lvl = reset_game(selected_level)
game_state = "menu"
space_pressed = False

running = True
while running:
    clock.tick(FPS)

    if game_state == "menu":
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Проверка кликов по кнопкам
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL1_BTN.collidepoint(event.pos):
                    selected_level = LevelOne
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                    space_pressed = False

                elif LEVEL2_BTN.collidepoint(event.pos):
                    selected_level = LevelTwo
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                    space_pressed = False

                elif LEVEL3_BTN.collidepoint(event.pos):
                    selected_level = LevelThree
                    player, level, curr_lvl = reset_game(selected_level)
                    game_state = "playing"
                    level.play_music()
                    space_pressed = False

            # Выход по ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

        # UI
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
                player, level, curr_lvl = reset_game(selected_level)
                game_state = "menu"
                space_pressed = False

    elif game_state == "victory":
        draw_victory(level.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player, level, curr_lvl = reset_game(selected_level)
                game_state = "menu"
                space_pressed = False

pygame.quit()
sys.exit()
