import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
MAROON = (128, 0, 0)  # Бардовый цвет
BLUE = (0, 0, 255)  # Цвет врагов
RED = (255, 0, 0)  # Цвет игрока

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простой Марио")

# Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Класс Врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)  # Враги синие
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed = -self.speed

# Класс Блока
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(MAROON)  # Стенки бардового цвета
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Класс Камеры
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        # Центрируем камеру на игроке
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Ограничение камеры
        x = min(0, x)
        x = max(-(self.width - WIDTH), x)
        y = min(0, y)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Функция для отображения текста
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surf.blit(text_surface, text_rect)

# Основной игровой цикл
def game_loop():
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Добавление блоков
    for x in range(0, 1600, 50):
        for y in range(0, 600, 50):
            if random.random() < 0.1:  # 10% вероятность создания блока
                block = Block(x, y)
                blocks.add(block)
                all_sprites.add(block)

    # Добавление врагов (уменьшено до 2)
    for _ in range(2):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Создание карты
    map_width, map_height = 1600, 1200
    camera = Camera(map_width, map_height)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()
        camera.update(player)

        # Проверка столкновений
        if pygame.sprite.spritecollideany(player, enemies):
            return False  # Вернуть False, если игрок столкнулся с врагом

        # Отображение
        screen.fill(DARK_GREEN)

        # Рисуем спрайты с учетом камеры
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()
        clock.tick(FPS)


# Экран проигрыша
def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_GREEN)
        draw_text(screen, "Игра окончена!", 50, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(screen, "Нажмите ESC для выхода", 30, WIDTH // 2, HEIGHT // 2 + 30)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

# Меню игры
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_GREEN)
        draw_text(screen, "Главное меню", 50, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(screen, "Нажмите ENTER для начала игры", 30, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text(screen, "Нажмите R для правил", 30, WIDTH // 2, HEIGHT // 2 + 70)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if game_loop() == False:
                game_over_screen()
        if keys[pygame.K_r]:
            show_rules()

# Функция для показа правил
def show_rules():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_GREEN)
        draw_text(screen, "Правила игры", 50, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, "1. Избегайте врагов!", 30, WIDTH // 2, HEIGHT // 2 - 10)
        draw_text(screen, "2. Двигайтесь по карте с помощью стрелок.", 30, WIDTH // 2, HEIGHT // 2 + 20)
        draw_text(screen, "3. Если столкнетесь с врагом - игра окончена.", 30, WIDTH // 2, HEIGHT // 2 + 60)
        draw_text(screen, "4. Нажмите ESC для выхода из правил.", 30, WIDTH // 2, HEIGHT // 2 + 100)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break

# Запуск игры
menu()
