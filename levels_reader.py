import pygame
from settings import SCREEN_WIDTH, RED

class LevelReader:
    def __init__(self, lvl, floor_y):
        self.floor_y = floor_y
        self.score = 0
        
        self.obstacles = []       # Список Rect для обычных шипов
        self.ceil_obstacles = []  # Список Rect для перевернутых шипов
        self.platforms = []       # Список Rect для блоков
        
        self.bg_image = pygame.transform.scale(lvl.bg_image, (SCREEN_WIDTH, self.floor_y + 50))
        
        BLOCK_SIZE = 40      
        START_OFFSET = 600   
        
        # Читаем всю сетку карты
        for row_index, row in enumerate(lvl.map):
            for col_index, char in enumerate(row):
                x = START_OFFSET + (col_index * BLOCK_SIZE)
                # Вычисляем Y сверху вниз: верх экрана — это row_index = 0
                y = row_index * BLOCK_SIZE
                
                if char == "P":
                    self.platforms.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "X":
                    self.obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == "M":
                    self.ceil_obstacles.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

    def update(self, game_speed):
        """Двигает абсолютно все типы объектов влево"""
        # Движение обычных шипов
        for spike in self.obstacles:
            spike.x -= game_speed
        self.obstacles = [s for s in self.obstacles if s.right > 0]

        # Движение перевернутых шипов
        for c_spike in self.ceil_obstacles:
            c_spike.x -= game_speed
        self.ceil_obstacles = [s for s in self.ceil_obstacles if s.right > 0]

        # Движение платформ
        for plat in self.platforms:
            plat.x -= game_speed
        self.platforms = [p for p in self.platforms if p.right > 0]

    def check_collisions(self, player_rect, player, game_speed):
        """Проверяет столкновения со всеми объектами на разной высоте"""
        
        # 1. Смерть от обычных шипов
        for spike in self.obstacles:
            if player_rect.colliderect(spike):
                return True
                
        # 2. Смерть от перевернутых шипов (потолочных)
        for c_spike in self.ceil_obstacles:
            if player_rect.colliderect(c_spike):
                return True
                
        # 3. Физика платформ (Приземление сверху)
        player.on_platform = False  
        
        for plat in self.platforms:
            if player_rect.colliderect(plat):
                # Если шарик летит вниз или стоит
                if player.vel_y >= 0:
                    # Проверяем, была ли нижняя точка шара выше платформы в прошлом кадре
                    if (player_rect.bottom - player.vel_y) <= plat.top + 5:
                        player.y = plat.top - player.size  # Ставим строго на крышу
                        player.vel_y = 0
                        player.is_jumping = False
                        player.on_platform = True
                        # Обновляем хитбокс игрока под новую безопасную координату Y
                        player_rect.y = player.y

        # 4. Проверка на удар боком (Смерть от стены)
        # Проверяем ТОЛЬКО те блоки, на которых мы сейчас НЕ стоим
        for plat in self.platforms:
            if player_rect.colliderect(plat) and not player.on_platform:
                # Если правый край шара заехал за левый край платформы
                if player_rect.right > plat.left and player_rect.left < plat.left:
                    # И мы находимся на уровне стены, а не пролетаем над ней
                    if player_rect.bottom > plat.top + 5:
                        return True # Честная смерть от удара в стену
                        
        return False


    def draw(self, screen):
        """Отрисовка всех объектов на своих персональных высотах"""
        # Линия основного пола
        pygame.draw.line(screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2)
        
        # 1. Рисуем блоки платформ
        for plat in self.platforms:
            pygame.draw.rect(screen, (140, 20, 140), plat) # Сделаем фиолетовыми, как на скрине
            pygame.draw.rect(screen, (0, 255, 255), plat, 1) # Голубая рамка
            
        # 2. Рисуем правильные шипы (треугольник острием вверх)
        for spike in self.obstacles:
            points = [(spike.left, spike.bottom), (spike.centerx, spike.top), (spike.right, spike.bottom)]
            pygame.draw.polygon(screen, RED, points)
            
        # 3. Рисуем перевернутые шипы (треугольник острием ВНИЗ)
        for c_spike in self.ceil_obstacles:
            points = [(c_spike.left, c_spike.top), (c_spike.centerx, c_spike.bottom), (c_spike.right, c_spike.top)]
            pygame.draw.polygon(screen, RED, points)
