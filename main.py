import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1200,850))

#Title, icon
pygame.display.set_caption("Kẻ_cướp_không_gian")
icon = pygame.image.load('D:/Python/Game/Logo.png')
pygame.display.set_icon(icon)
# Background
backgroundImg = pygame.image.load('D:/Python/Game/background.png')
backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

#Player
playerImg = pygame.image.load('D:/Python/Game/arcade_space.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))  
playerX = (1200 - 100) // 2  
playerY = 693  # Vị trí giữa khoảng (650 + 736) / 2
playerX_change = 0
playerY_change = 0
def player(x, y):
    screen.blit(playerImg, (x, y)) #chèn player vào

#Enemy
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('D:/Python/Game/ghost.png')
        self.img = pygame.transform.scale(self.img, (65, 65))
        self.reset_position()
        self.speed = 0.08

    def reset_position(self):
        self.x = random.randint(0, 1135)  # 1200 - 65 (kích thước enemy)
        self.y = random.randint(-100, -50)  # Spawn phía trên màn hình

    def move(self):
        self.y += self.speed
        # Nếu enemy ra khỏi màn hình, reset lại vị trí
        if self.y > 850:
            self.reset_position()

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

# Tạo list chứa nhiều enemy
enemies = [Enemy() for _ in range(2)]  # Tạo 5 enemy

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
    #màu nền
    # screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))


    # Vẽ đường kẻ trắng để phân định giới hạn
    boundary_y = 650  # Đặt giới hạn gần với vị trí ban đầu của player hơn
    pygame.draw.line(screen, (255, 255, 255), (0, boundary_y), (1200, boundary_y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #điều khiển player bằng phím
        #Sang trái phải
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.2 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        #Lên xuống
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change -= 0.2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerY_change = 0.2
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

    # Giới hạn player chỉ di chuyển bên dưới đường kẻ trắng
    if playerY <= boundary_y:  # Sử dụng biến boundary_y thay vì số cứng
        playerY = boundary_y
    elif playerY >= 736:
        playerY = 736

    # Cập nhật và vẽ enemies
    for enemy in enemies:
        enemy.move()
        enemy.draw(screen)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 800
        bullet_state = "ready"

    player(playerX, playerY)
    pygame.display.update()
