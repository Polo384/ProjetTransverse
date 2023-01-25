import pygame
import sys
from functions import *

# Initialisation
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

# Title and icon
pygame.display.set_caption('DWARF')
icon = pygame.image.load('DWARF/icon/icon.png')
pygame.display.set_icon(icon)

# Game loop
running = True
i=0
while running:
    i+=1
    print(i)  
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