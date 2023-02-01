import pygame, ctypes, sys
from functions import *
ctypes.windll.user32.SetProcessDPIAware() # To adapt to screen size

def if_matrix(right,left,down,up):
    global map_matrix, i, j
    if map_matrix[i][j+1] == right and map_matrix[i][j-1] == left and map_matrix[i-1][j] == down and map_matrix[i+1][j] == up:
        return True
    else:
        return False
        
# Initialisation
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1920,1080), pygame.SCALED)

# Title and icon
pygame.display.set_caption('DWARF')
icon = pygame.image.load('DWARF/icon/icon.png')
pygame.display.set_icon(icon)

# Game loop
running = True
while running:
    screen.fill((0,0,0))
        

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:   # Press k to exit (c'est utile pour moi j'ai le bouton k sur ma souris mdr)
                    pygame.quit()
                    sys.exit()
    pygame.display.update()