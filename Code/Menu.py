import pygame
import button


pygame.init()

#create game window
SCREEN_WIDTH =   1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 85)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("D:/Python/Game/images/button_resume.png").convert_alpha()
options_img = pygame.image.load("D:/Python/Game/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()

#create button instances
resume_button = button.Button(535, 210, resume_img,1)
options_button = button.Button(528, 350, options_img,1)
quit_button = button.Button(562, 485, quit_img,1)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
running = True
while running:
    screen.fill((0,0,0))
    #check if game is paused
    if game_paused == True:
      if resume_button.draw(screen):
         game_paused = False
      if options_button.draw(screen):
         pass
      if quit_button.draw(screen):
         running = False

      #display menu
    else:
      draw_text("CHAN ĐÊ", font, TEXT_COL, 390, 250)
  #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True
        if event.type == pygame.QUIT:
            running = False
  



    pygame.display.update()
pygame.quit()
