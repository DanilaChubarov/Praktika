import os
import sys
import pygame

# 1. Вычисляем корень проекта (поднимаемся на 2 уровня вверх из media/maps)
current_dir = os.path.dirname(os.path.abspath(__file__))
media_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(media_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

pygame.init()

# Настройки сетки
BLOCK_SIZE = 40
GRID_ROWS = 12  # Высота вашей игровой сетки (500 // 40)
GRID_COLS = 300 # Изначальная длина уровня (расширится автоматически при импорте)
FPS = 60

# Имя файла для импорта/экспорта (лежит в той же папке maps)
MAP_FILE_NAME = "level3_map.txt"
map_path = os.path.join(current_dir, MAP_FILE_NAME)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash - Продвинутый Редактор")
clock = pygame.time.Clock()

# Палитра объектов
PALETTE = [
    {"char": ".", "color": (30, 30, 30), "name": "Ластик"},
    {"char": "P", "color": (140, 20, 140), "name": "Блок P"},
    {"char": "S", "color": (100, 10, 100), "name": "Полублок S"},
    {"char": "X", "color": (255, 50, 50), "name": "Шип X"},
    {"char": "M", "color": (200, 30, 30), "name": "Потолок M"},
    {"char": "G", "color": (0, 255, 0), "name": "Грави-орб G"},
    {"char": "D", "color": (0, 200, 255), "name": "Прыжок D"}
]
current_palette_index = 1

# --- ЛОГИКА ИМПОРТА УРОВНЯ ---
level_grid = []
if os.path.exists(map_path):
    print(f"Обнаружен существующий уровень! Загружаю {MAP_FILE_NAME}...")
    try:
        with open(map_path, "r", encoding="utf-8") as file:
            for line in file:
                # Очищаем от переносов строк и преобразуем в список символов
                row_chars = list(line.strip('\n'))
                if row_chars:
                    level_grid.append(row_chars)
        
        # Обновляем размеры сетки на основе загруженного файла
        GRID_ROWS = len(level_grid)
        GRID_COLS = max(len(row) for row in level_grid)
        print(f"Успешно загружено! Размер карты: {GRID_COLS}x{GRID_ROWS} блоков.")
    except Exception as e:
        print(f"Ошибка при чтении файла, создаю пустую карту. Ошибка: {e}")

# Если файла не было или он поврежден — создаем пустую сетку
if not level_grid:
    print("Файл карты не найден. Создаю чистый холст...")
    level_grid = [["." for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Камера
camera_x = 0
scroll_speed = 15

def save_level():
    """Сохранение сетки в файл"""
    with open(map_path, "w", encoding="utf-8") as file:
        for row in level_grid:
            file.write("".join(row) + "\n")
    print(f"Уровень сохранен в: {map_path}")

# Вычисляем позиции кнопок палитры на нижней панели (HUD)
hud_y = SCREEN_HEIGHT - 60
btn_width = 110
btn_height = 40
start_btn_x = 20

running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    # Скроллинг камеры
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x += scroll_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x = max(0, camera_x - scroll_speed)

    # ОБРАБОТКА ИВЕНТОВ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_7:
                current_palette_index = event.key - pygame.K_1
            if event.key == pygame.K_s:
                save_level()

        # Клик мыши (Проверяем UI палитры)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Если кликнули в зоне нижней панели HUD
            if mouse_pos[1] >= hud_y:
                for idx, item in enumerate(PALETTE):
                    btn_x = start_btn_x + idx * (btn_width + 10)
                    btn_rect = pygame.Rect(btn_x, hud_y + 10, btn_width, btn_height)
                    if btn_rect.collidepoint(mouse_pos):
                        current_palette_index = idx
                        break

    # РИСОВАНИЕ НА СЕТКЕ (Зажатая мышь работает только выше панели HUD)
    if mouse_pos[1] < hud_y:
        mouse_buttons = pygame.mouse.get_pressed()
        grid_x = (mouse_pos[0] + camera_x) // BLOCK_SIZE
        grid_y = mouse_pos[1] // BLOCK_SIZE
        
        if 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS:
            if mouse_buttons[0]:    # ЛКМ — ставим блок
                level_grid[grid_y][grid_x] = PALETTE[current_palette_index]["char"]
            elif mouse_buttons[2]:  # ПКМ — стираем блок
                level_grid[grid_y][grid_x] = "."

    # --- ОТРИСОВКА ЭКРАНА ---
    screen.fill(BLACK)
    
    # 1. Отрисовка игрового поля и блоков
    for row_idx in range(GRID_ROWS):
        for col_idx in range(GRID_COLS):
            x = col_idx * BLOCK_SIZE - camera_x
            y = row_idx * BLOCK_SIZE
            
            if x < -BLOCK_SIZE or x > SCREEN_WIDTH:
                continue
                
            char = level_grid[row_idx][col_idx]
            
            color = (30, 30, 30)
            for item in PALETTE:
                if item["char"] == char:
                    color = item["color"]
                    break
            
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, rect)
            
            if char == ".":
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)
            else:
                pygame.draw.rect(screen, WHITE, rect, 1)

    # 2. Отрисовка нижней панели интерфейса (HUD)
    pygame.draw.rect(screen, (15, 15, 15), (0, hud_y, SCREEN_WIDTH, 60))
    pygame.draw.line(screen, WHITE, (0, hud_y), (SCREEN_WIDTH, hud_y), 2)
    
    font = pygame.font.SysFont(None, 20)
    
    # Рисуем интерактивные кнопки элементов
    for idx, item in enumerate(PALETTE):
        btn_x = start_btn_x + idx * (btn_width + 10)
        btn_rect = pygame.Rect(btn_x, hud_y + 10, btn_width, btn_height)
        
        # Заливка кнопки цветом элемента
        pygame.draw.rect(screen, item["color"], btn_rect)
        
        # Если элемент выбран — рисуем жирную белую рамку вокруг кнопки
        if idx == current_palette_index:
            pygame.draw.rect(screen, WHITE, btn_rect, 3)
        else:
            pygame.draw.rect(screen, (100, 100, 100), btn_rect, 1)
            
        # Текст на кнопке
        text_surf = font.render(item["name"], True, WHITE)
        screen.blit(text_surf, (btn_rect.x + 8, btn_rect.y + 12))

    # Информация о клавишах в правом углу панели
    info_font = pygame.font.SysFont(None, 18)
    save_text = info_font.render("Нажми [S] для сохранения", True, (200, 200, 200))
    cam_text = info_font.render(f"Камера X: {camera_x} (A/D)", True, (200, 200, 200))
    screen.blit(save_text, (SCREEN_WIDTH - 180, hud_y + 15))
    screen.blit(cam_text, (SCREEN_WIDTH - 180, hud_y + 35))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
