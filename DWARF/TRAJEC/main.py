import pygame
import math
from playerclass2 import *
from projectilesclass2 import *

heightscreen = 500
widthscreen = 1200

screen = pygame.display.set_mode((widthscreen, heightscreen))
pygame.display.set_caption('Test projectile')

def redrawwindow():
    screen.fill((64, 64, 64))
    player1.draw(screen)
    player1.cursor(screen)
    player1.update()
    player1.handle_events()
    if player1.ball:
        player1.ball.draw(screen)
    print(player1.angle)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
white = (255, 255, 255)
player1 = Player(200, 400, white)
pygame.display.flip()

while run:
    clock.tick(60)
    redrawwindow()

pygame.quit()
quit()
