import pygame
from settings import SCREEN_HEIGHT, CYAN
from levels_reader import GameState


class Player:
    def __init__(self, lvl, x, floor_y):
        self.size = 40
        self.x = x
        self.floor_y = floor_y
        self.y = floor_y - self.size
        self.game_speed = lvl.lvl_speed

        self.vel_y = 0
        self.gravity = 1
        self.jump_strength = -14
        self.is_jumping = False
        self.can_jump = True
        self.angle = 0
        self.on_platform = False
        self.was_in_air = False  # Флаг для отслеживания приземления
        self.just_landed = False  # Флаг для защиты от дребезга
        self.used_orb = False
        self.texture_path="media/textures/basket_ball.png"
        self.wave_trail = []       # Список для хранения координат (x, y)
        self.max_trail_length = 60 # Длина следа в кадрах (примерно 1 секунда при 60 FPS)
        # Загрузка текстуры
        self.texture = pygame.image.load(
            self.texture_path
        ).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.size, self.size))

    def jump(self):
        """Прыгает"""
        if self.can_jump:
            self.vel_y = self.jump_strength
            self.is_jumping = True
            self.can_jump = False

    def update(self, game_mode, space_held=False):
        if game_mode==GameState.CUBE:
            # Гравитация
            self.vel_y += self.gravity
            self.y += self.vel_y

            # Проверка пола
            if self.y >= self.floor_y - self.size:
                self.y = self.floor_y - self.size
                self.vel_y = 0
                self.is_jumping = False
                self.can_jump = True
                self.on_platform = True

                # Если пробел зажат И мы были в воздухе И не только что приземлились
                if space_held and self.was_in_air and not self.just_landed:
                    self.jump()
                    self.just_landed = True

                self.was_in_air = False
            else:
                # Мы в воздухе
                # Мы в воздухе
                self.was_in_air = True
                self.just_landed = False
                self.on_platform = False

            if self.gravity < 0 and self.y <= 0:
                self.y = 0
                self.vel_y = 0
                self.is_jumping = False
                self.can_jump = True

                # Автопрыжок от потолка
                if space_held:
                    self.jump()

            # Вращение
            if self.gravity > 0:
                if not self.is_jumping:
                    self.angle -= self.game_speed * 1.5
                else:
                    self.angle -= 5
            if self.gravity < 0:
                if not self.is_jumping:
                    self.angle += self.game_speed * 1.5
                else:
                    self.angle += 5
        if game_mode==GameState.SHIP:
            airplane_force = 0.5 if self.gravity > 0 else -0.5
            if space_held:
                # При зажатом пробеле летим против текущей гравитации
                self.vel_y -= airplane_force * 2.5
            else:
                # Когда пробел отпущен, действует обычная гравитация
                self.vel_y += self.gravity
            
            # Ограничение максимальной скорости взлёта/падения
            max_speed = 8
            self.vel_y = max(-max_speed, min(self.vel_y, max_speed))
            
            # ВАЖНО: Применяем высчитанную скорость к координате Y!
            self.y += self.vel_y

            # Ограничение пола для корабля
            if self.y >= self.floor_y - self.size:
                self.y = self.floor_y - self.size
                self.vel_y = 0

            # Ограничение потолка для корабля (y = 0)
            if self.y <= 0:
                self.y = 0
                self.vel_y = 0

            # Плавный наклон корабля по направлению движения
            # Вверх летит — нос задирается, вниз падает — опускается
            target_angle = -self.vel_y * 4 if self.gravity > 0 else self.vel_y * 4
            self.angle += (target_angle - self.angle) * 0.2
        elif game_mode == GameState.WAVE:
            # --- РЕЖИМ ВОЛНЫ ---
            # Скорость волны должна быть завязана на скорость игры, чтобы угол всегда был 45 градусов.
            # Если ваша волна двигается по оси X со скоростью self.game_speed, то и по Y она должна лететь с такой же скоростью.
            wave_speed = self.game_speed

            if space_held:
                # При зажатом пробеле летим вверх (вниз при инвертированной гравитации)
                self.vel_y = -wave_speed if self.gravity > 0 else wave_speed
                self.angle = 45 if self.gravity > 0 else -45
            else:
                # Когда пробел отпущен, падаем вниз (вверх при инвертированной гравитации)
                self.vel_y = wave_speed if self.gravity > 0 else -wave_speed
                self.angle = -45 if self.gravity > 0 else 45

            # Применяем скорость к координате Y
            self.y += self.vel_y

            # Ограничение пола (волна мгновенно скользит по полу горизонтально)
            if self.y >= self.floor_y - self.size:
                self.y = self.floor_y - self.size
                self.vel_y = 0
                self.angle = 0  # Прижимается к полу ровно

            # Ограничение потолка (волна мгновенно скользит по потолку горизонтально)
            if self.y <= 0:
                self.y = 0
                self.vel_y = 0
                self.angle = 0  # Прижимается к потолку ровно
            self.wave_trail = [(x - self.game_speed, y) for x, y in self.wave_trail]
        
            # 2. Добавляем текущую позицию центра волны (или ее задней части)
            # Предполагаем, что self.x — это горизонтальная позиция игрока на экране (обычно фиксированная)
            trail_x = self.x + self.size / 2
            trail_y = self.y + self.size / 2
            self.wave_trail.append((trail_x, trail_y))
            
            # 3. Обрезаем след, если он стал слишком длинным
            if len(self.wave_trail) > self.max_trail_length:
                self.wave_trail.pop(0)
            else:
                # Если режим сменился, плавно или мгновенно очищаем след
                if self.wave_trail:
                    self.wave_trail.clear()
    def fly(self, space_held):
        """Физика полета для режима корабля (SHIP)"""
        # Константы для настройки физики корабля (можно вынести в settings.py)
        THRUST = 0.6         # Сила подъема вверх при зажатом пробеле
        GRAVITY_SHIP = 0.45  # Сила падения вниз (обычно мягче, чем у куба)
        MAX_SPEED_Y = 6      # Максимальная скорость взлета/падения

        if space_held:
            # Тяга вверх: уменьшаем vel_y (в Pygame минус — это вверх)
            self.vel_y -= THRUST
        else:
            # Падение: увеличиваем vel_y под действием гравитации корабля
            self.vel_y += GRAVITY_SHIP

        # Ограничиваем скорость, чтобы корабль управлялся адекватно
        if self.vel_y > MAX_SPEED_Y:
            self.vel_y = MAX_SPEED_Y
        elif self.vel_y < -MAX_SPEED_Y:
            self.vel_y = -MAX_SPEED_Y

        # Применяем изменение позиции
        self.y += self.vel_y

    def draw(self, screen):
        rotated_ball = pygame.transform.rotate(self.texture, self.angle)
        rect = rotated_ball.get_rect()
        rect.center = (self.x + self.size // 2, self.y + self.size // 2)
        screen.blit(rotated_ball, rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x + 3, self.y + 3, self.size - 12, self.size - 12)
