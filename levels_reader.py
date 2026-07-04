import pygame
from settings import SCREEN_WIDTH, RED

class LevelReader:
    def __init__(self, lvl, floor_y):
        self.floor_y = floor_y
        self.score = 0
        self.world_offset = 0  # Отслеживание прогресса уровня
        self.game_speed = lvl.lvl_speed
        self.obstacles = []       # Список Rect для обычных шипов
        self.ceil_obstacles = []  # Список Rect для перевернутых шипов
        self.platforms = []       # Список Rect для блоков
        self.slabs = [] #Список полублоков
        
        self.bg_image = pygame.transform.scale(lvl.bg_image, (SCREEN_WIDTH, self.floor_y + 50))
        self.bg_x1= lvl.bg_x1
        self.bg_x2= lvl.bg_x2
        self.bg_speed=lvl.bg_speed
        
        #Активация музыки
        pygame.mixer.music.load(lvl.music_name)
        
        BLOCK_SIZE = 40      
        START_OFFSET = 0  
        
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
                elif char == "S":
                    self.slabs.append(pygame.Rect(x, y,BLOCK_SIZE, BLOCK_SIZE//2 ))

    def update(self):
        """Двигает абсолютно все типы объектов влево"""
        #Движение фона
        
        self.bg_x1 -= self.bg_speed
        self.bg_x2 -= self.bg_speed
        if self.bg_x1 <= -SCREEN_WIDTH:
            self.bg_x1 = self.bg_x2 + SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH:
            self.bg_x2 = self.bg_x1 + SCREEN_WIDTH
            
        # Увеличиваем счетчик прогресса
        self.world_offset += self.game_speed
        self.score += self.game_speed  # Счет зависит от прогресса
        
        # Движение обычных шипов
        for spike in self.obstacles:
            spike.x -= self.game_speed
        self.obstacles = [s for s in self.obstacles if s.right > 0]

        # Движение перевернутых шипов
        for c_spike in self.ceil_obstacles:
            c_spike.x -= self.game_speed
        self.ceil_obstacles = [s for s in self.ceil_obstacles if s.right > 0]

        # Движение платформ
        for plat in self.platforms:
            plat.x -= self.game_speed
        self.platforms = [p for p in self.platforms if p.right > 0]
        
        #Движение полублоков
        for slab in self.slabs:
            slab.x -= self.game_speed
        self.slabs = [s for s in self.slabs if s.right > 0]
        
        #Движение 

    def check_collisions(self, player_rect, player, space_held=False):
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
        
        for plat in self.platforms + self.slabs:
            if player_rect.colliderect(plat):
                # Если шарик летит вниз или стоит
                if player.vel_y >= 0:
                    # Проверяем, была ли нижняя точка шара выше платформы в прошлом кадре
                    if (player_rect.bottom - player.vel_y) <= plat.top + 5:
                        player.y = plat.top - player.size  # Ставим строго на крышу
                        player.vel_y = 0
                        player.is_jumping = False
                        player.can_jump = True
                        player.on_platform = True
                        
                        # Если пробел зажат И мы были в воздухе И не только что приземлились
                        if space_held and player.was_in_air and not player.just_landed:
                            player.jump()
                            player.just_landed = True
                        
                        player.was_in_air = False
                        
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
        #1. Рисуем задний фон
        screen.blit(self.bg_image, (self.bg_x1, 0))
        screen.blit(self.bg_image, (self.bg_x2, 0))
        #2 Линия основного пола
        pygame.draw.line(screen, (255, 255, 255), (0, self.floor_y), (SCREEN_WIDTH, self.floor_y), 2)
        
        # 3. Рисуем блоки платформ
        for plat in self.platforms:
            pygame.draw.rect(screen, (140, 20, 140), plat) # Сделаем фиолетовыми, как на скрине
            pygame.draw.rect(screen, (0, 255, 255), plat, 1) # Голубая рамка
        
        for slab in self.slabs:
            pygame.draw.rect(screen, (140, 20, 140), slab) # Сделаем фиолетовыми, как на скрине
            pygame.draw.rect(screen, (0, 255, 255), slab, 1) # Голубая рамка
            
        # 4. Рисуем правильные шипы (треугольник острием вверх)
        for spike in self.obstacles:
            points = [(spike.left, spike.bottom), (spike.centerx, spike.top), (spike.right, spike.bottom)]
            pygame.draw.polygon(screen, RED, points)
            
        # 5. Рисуем перевернутые шипы (треугольник острием ВНИЗ)
        for c_spike in self.ceil_obstacles:
            points = [(c_spike.left, c_spike.top), (c_spike.centerx, c_spike.bottom), (c_spike.right, c_spike.top)]
            pygame.draw.polygon(screen, RED, points)
    def play_music(self):
        pygame.mixer.music.play(-1)