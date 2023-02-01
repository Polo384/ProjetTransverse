import pygame, pymunk, sys
from functions import *

def create_player(player_mask):
    mask = pymunk.Poly.create_box(None, (50, 50))
    body = pymunk.Body(1, 10000)
    shape_vertices = [(v[0], v[1]) for v in player_mask.outline()]
    shape = pymunk.Poly(body, shape_vertices)
    body.position = (400,0)
    #shape = pymunk.Shape(body, player_mask)
    space.add(body,shape)
    return shape

def draw_player(players, player_image):
    for player in players:
        pos_x = int(player.body.position.x)
        pos_y = int(player.body.position.y)
        screen.blit(player_image, (pos_x, pos_y),80)

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,500)
player_image = pygame.image.load("DWARF/icon/icon.png").convert_alpha()
player_image = scale(player_image, 'div', 20)
player_mask = get_mask(player_image)
players = []
players.append(create_player(space))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((217,217,217))
    draw_player(players, player_image)
    space.step(1/50)
    pygame.display.update()
    clock.tick(60)