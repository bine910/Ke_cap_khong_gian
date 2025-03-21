import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1200,850))

#Title, icon
pygame.display.set_caption("Kẻ_cướp_không_gian")
icon = pygame.image.load('D:/Python/Game/Logo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('D:/Python/Game/arcade_space.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))  
playerX = (1200 - 100) // 2  
playerY = 850 - 200          
playerX_change = 0
playerY_change = 0
def player(x, y):
    screen.blit(playerImg, (x, y)) #chèn player vào

#Enermy
enermyImg = pygame.image.load('D:/Python/Game/ghost.png')
enermyImg = pygame.transform.scale(enermyImg, (65, 65))  
enermyX = random.randint(0, 1200)
enermyY = random.randint(50, 450)
enermyX_change = 0.1
enermyY_change = 0.1

def enermy(x, y):
    screen.blit(enermyImg, (x, y)) #chèn enermy vào

#Bullet
bulletImg = pygame.image.load('D:/Python/Game/bullet.png')
bulletX = 0
bulletY = 800
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 50 - 16, y - 10))

#Game loop
running = True
while running:
    #màu 
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #điều khiển player bằng phím
        #Sang trái phải
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        #Lên xuống
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change -= 0.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerY_change = 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    
        #Bắn bằng phím space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
    
    playerX += playerX_change
    playerY += playerY_change

    #Boundary limit
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1100:
        playerX = 1100

    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    enermyX += enermyX_change
    enermyY += enermyY_change
    if enermyX <= 0 or enermyX >= 1100:
        enermyX_change *= -1
    if enermyY <= 0 or enermyY >= 450:
        enermyY_change *= -1

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 800
        bullet_state = "ready"

    player(playerX, playerY)
    enermy(enermyX, enermyY)    
    pygame.display.update()
