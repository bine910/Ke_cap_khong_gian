import pygame

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


#Game loop
running = True
while running:
    #màu 
    screen.fill((20, 0, 10))

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
    
    playerX += playerX_change
    playerY += playerY_change
    #boundary limit
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1100:
        playerX = 1100

    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    player(playerX, playerY)
    pygame.display.update()