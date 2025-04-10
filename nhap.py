import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1200, 850))
pygame.display.set_caption("Kẻ_cướp_không_gian")
icon = pygame.image.load('D:/Python/Game/Logo.png')
pygame.display.set_icon(icon)

# Load hình ảnh
backgroundImg = pygame.image.load('D:/Python/Game/background.png')
backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))
playerImg = pygame.image.load('D:/Python/Game/arcade_space.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))
enemyImg = pygame.image.load('D:/Python/Game/ghost.png')
enemyImg = pygame.transform.scale(enemyImg, (65, 65))
bulletImg = pygame.image.load('D:/Python/Game/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (34, 34))
bottoImg = pygame.image.load('D:/Python/Game/robot.png')
bottoImg = pygame.transform.scale(bottoImg, (100, 100))

# Thông tin player
playerX = (1200 - 100) // 2
playerY = 693
player_speed = 1
move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

def draw_player(x, y):
    screen.blit(playerImg, (x, y))

def draw_enemy(enemy):
    screen.blit(enemyImg, (enemy['x'], enemy['y']))

def draw_botto(boss):
    screen.blit(bottoImg, (boss['x'], boss['y']))

def fire_bullet(x, y):
    return {'x': x + 50 - 17, 'y': y - 34, 'state': 'fire'}

def fire_boss_bullets(boss, playerX, playerY):
    bullets = []
    for _ in range(random.randint(3, 5)):
        angle = math.atan2(playerY - boss['y'], playerX - boss['x']) + random.uniform(-0.3, 0.3)
        speed = 2 + random.random()
        bullets.append({
            'x': boss['x'] + 50,
            'y': boss['y'] + 100,
            'dx': math.cos(angle) * speed,
            'dy': math.sin(angle) * speed
        })
    return bullets

def is_collision(obj1, obj2, size=40):
    distance = math.hypot(obj1['x'] - obj2['x'], obj1['y'] - obj2['y'])
    return distance < size

# Cấu hình level
MAX_LEVEL = 10
level = 1
level_timer = 0
level_duration = 1500  # Frames

# Danh sách enemy & bullet
enemies = []
bosses = []
bullets = []
boss_bullets = []

# Cấu hình enemy theo level
def get_enemy_stats(level):
    base_hp = 1 + level // 3
    speed = max(0.3, 1.5 - level * 0.1)
    count = min(6 + level, 20)
    return base_hp, speed, count

def spawn_enemies(level):
    enemies = []
    hp, speed, count = get_enemy_stats(level)
    for i in range(count):
        enemies.append({
            'x': random.randint(50, 1150),
            'y': random.randint(-800, -100),
            'speed': speed * random.uniform(0.8, 1.2),
            'hp': hp
        })
    return enemies

def spawn_boss(level):
    if level < 3:
        return []
    return [{
        'x': random.randint(100, 1100),
        'y': -120,
        'speed': 0.5,
        'hp': 5 + level,
        'cooldown': 0
    }]

# Game loop
running = True
clock = pygame.time.Clock()
bullet_cooldown = 0

# Khởi tạo
enemies = spawn_enemies(level)
bosses = spawn_boss(level)

while running:
    screen.blit(backgroundImg, (0, 0))
    pygame.draw.line(screen, (255, 255, 255), (0, 650), (1200, 650), 2)
    level_timer += 1

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a): move_direction['left'] = True
            if event.key in (pygame.K_RIGHT, pygame.K_d): move_direction['right'] = True
            if event.key in (pygame.K_UP, pygame.K_w): move_direction['up'] = True
            if event.key in (pygame.K_DOWN, pygame.K_s): move_direction['down'] = True
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if bullet_cooldown == 0:
                    bullets.append(fire_bullet(playerX, playerY))
                    bullet_cooldown = 15
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a): move_direction['left'] = False
            if event.key in (pygame.K_RIGHT, pygame.K_d): move_direction['right'] = False
            if event.key in (pygame.K_UP, pygame.K_w): move_direction['up'] = False
            if event.key in (pygame.K_DOWN, pygame.K_s): move_direction['down'] = False

    # Di chuyển player
    if move_direction['left']: playerX -= player_speed
    if move_direction['right']: playerX += player_speed
    if move_direction['up']: playerY -= player_speed
    if move_direction['down']: playerY += player_speed
    playerX = max(0, min(playerX, 1200 - 100))
    playerY = max(650, min(playerY, 850 - 100))

    # Đạn player
    if bullet_cooldown > 0:
        bullet_cooldown -= 1
    for b in bullets[:]:
        b['y'] -= 5
        screen.blit(bulletImg, (b['x'], b['y']))
        if b['y'] < 0:
            bullets.remove(b)

    # Enemy thường
    for e in enemies[:]:
        e['y'] += e['speed']
        draw_enemy(e)
        for b in bullets[:]:
            if is_collision(e, b):
                e['hp'] -= 1
                bullets.remove(b)
                if e['hp'] <= 0:
                    enemies.remove(e)
                    break

    # Bot to
    for boss in bosses[:]:
        boss['y'] += boss['speed']
        draw_botto(boss)

        # Boss bắn đạn
        if boss['cooldown'] <= 0:
            boss_bullets.extend(fire_boss_bullets(boss, playerX, playerY))
            boss['cooldown'] = 120
        else:
            boss['cooldown'] -= 1

        for b in bullets[:]:
            if is_collision(boss, b, 60):
                boss['hp'] -= 1
                bullets.remove(b)
                if boss['hp'] <= 0:
                    bosses.remove(boss)
                    break

    # Đạn từ boss
    for bb in boss_bullets[:]:
        bb['x'] += bb['dx']
        bb['y'] += bb['dy']
        pygame.draw.circle(screen, (255, 50, 50), (int(bb['x']), int(bb['y'])), 5)
        if bb['y'] > 900 or bb['x'] < 0 or bb['x'] > 1200:
            boss_bullets.remove(bb)

    # Chuyển level
    if level_timer >= level_duration:
        level_timer = 0
        if level < MAX_LEVEL:
            level += 1
            enemies = spawn_enemies(level)
            bosses = spawn_boss(level)

    # Hiển thị level
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level {level}", True, (255, 255, 255))
    screen.blit(level_text, (20, 20))

    draw_player(playerX, playerY)
    pygame.display.update()
    clock.tick(240)

pygame.quit()
