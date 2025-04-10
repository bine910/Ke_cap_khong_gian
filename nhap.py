import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1200,850))

# Title, icon
pygame.display.set_caption("Kẻ_cướp_không_gian")
icon = pygame.image.load('D:/Python/Game/Logo.png')
pygame.display.set_icon(icon)

# Background
backgroundImg = pygame.image.load('D:/Python/Game/background.png')
backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

# Player
playerImg = pygame.image.load('D:/Python/Game/arcade_space.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))  
playerX = (1200 - 100) // 2  
playerY = 693
player_speed = 1
move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = pygame.image.load('D:/Python/Game/ghost.png')
enemyImg = pygame.transform.scale(enemyImg, (65, 65))  
enemy_speed = 0.5
max_enemies = 5
enemies = []

# Initialize enemies
def init_enemies():
    for i in range(max_enemies):
        # Space enemies vertically with at least 100 pixels between them
        spawn_y = -100 - (i * 150)  # Start above screen with spacing
        spawn_x = random.randint(50, 1150)
        enemies.append({
            'x': spawn_x,
            'y': spawn_y,
            'speed': enemy_speed * random.uniform(0.8, 1.2)  # Slightly varied speeds
        })

init_enemies()

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Bullet
bulletImg = pygame.image.load('D:/Python/Game/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (34, 34)) 
bulletX = 0
bulletY = 800
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state, bulletX, bulletY
    bullet_state = "fire"
    bulletX = x + playerImg.get_width()//2 - bulletImg.get_width()//2
    bulletY = y - bulletImg.get_height()

# Game loop
running = True
clock = pygame.time.Clock()
spawn_timer = 0

while running:
    # Màu nền
    screen.blit(backgroundImg, (0, 0))

    # Vẽ đường kẻ trắng để phân định giới hạn
    boundary_y = 650
    pygame.draw.line(screen, (255, 255, 255), (0, boundary_y), (1200, boundary_y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # Điều khiển player bằng phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_direction['left'] = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_direction['right'] = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_direction['up'] = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_direction['down'] = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if bullet_state == "ready":
                    fire_bullet(playerX, playerY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_direction['left'] = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_direction['right'] = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_direction['up'] = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_direction['down'] = False
    
    # Cập nhật vị trí player
    if move_direction['left']:
        playerX -= player_speed
    if move_direction['right']:
        playerX += player_speed
    if move_direction['up']:
        playerY -= player_speed
    if move_direction['down']:
        playerY += player_speed

    # Boundary limit
    playerX = max(0, min(playerX, 1200 - playerImg.get_width()))
    playerY = max(boundary_y, min(playerY, 850 - playerImg.get_height()))

    # Bullet movement
    if bullet_state == "fire":
        bulletY -= bulletY_change
        screen.blit(bulletImg, (bulletX, bulletY))
        if bulletY <= 0:
            bullet_state = "ready"
    
    # Enemy movement and spawning
    spawn_timer += 1
    if spawn_timer >= 180 and len(enemies) < max_enemies:  # Spawn new enemy every ~3 seconds if under limit
        spawn_timer = 0
        spawn_y = -100
        spawn_x = random.randint(50, 1150)
        enemies.append({
            'x': spawn_x,
            'y': spawn_y,
            'speed': enemy_speed * random.uniform(0.8, 1.2)
        })
    
    # Update and draw enemies
    for enemy_data in enemies[:]:
        enemy_data['y'] += enemy_data['speed']
        enemy(enemy_data['x'], enemy_data['y'])
        
        # Remove enemies that go off screen
        if enemy_data['y'] > 900:
            enemies.remove(enemy_data)
            # When one enemy is removed, potentially spawn a new one
            if random.random() < 0.7:  # 70% chance to spawn new enemy when one leaves
                spawn_y = -100
                spawn_x = random.randint(50, 1150)
                enemies.append({
                    'x': spawn_x,
                    'y': spawn_y,
                    'speed': enemy_speed * random.uniform(0.8, 1.2)
                })
    
    player(playerX, playerY)
    pygame.display.update()
    clock.tick(240)

pygame.quit()
