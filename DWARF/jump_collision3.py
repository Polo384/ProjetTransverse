import pygame
import pymunk
from functions import *

# Initialisation de pygame et pymunk
pygame.init()
space = pymunk.Space()

# Taille de la fenêtre
screen_size = (800, 600)
clock = pygame.time.Clock()

# Création de la fenêtre
screen = pygame.display.set_mode(screen_size)

# Position initiale du personnage
player_pos = [400, 0]

# Chargement de l'image du personnage
player_image = pygame.image.load("DWARF/icon/icon.png").convert_alpha()
player_image = scale(player_image, 'div', 20)
player_rect = player_image.get_rect()

# Vitesse de déplacement du personnage
player_speed = 3

# Position initiale du sol
ground_pos = [0,0]

# Chargement de l'image du sol
ground_image = pygame.image.load("DWARF/ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, screen_size)
scaled_ground_image = pygame.transform.scale(ground_image, (ground_image.get_width()*4, ground_image.get_height()*1))
ground_image = scaled_ground_image
ground_rect = ground_image.get_rect()

# Création des formes pour les collisions
player_shape = pymunk.Poly.create_box(None, player_rect.size)
ground_shape = pymunk.Poly.create_box(None, ground_rect.size)

# Attachement des formes aux positions
player_shape.body = pymunk.Body(1, 1000000)
player_shape.body.position = player_pos
ground_shape.body = pymunk.Body(1000000, 1000000)
ground_shape.body.position = ground_pos

# Ajout des formes à l'espace de collision
space.add(player_shape.body, player_shape, ground_shape.body, ground_shape)

# Boucle principale
running = True
player_on_ground = False  # added variable to keep track of player on ground
gravity = 2
mult = 1
jump_flag = False
player_pos_save = player_pos
while running:
    screen.fill((0, 0, 0))
    player_on_ground = False
    # Détection des touches pressées
    keys = pygame.key.get_pressed()

    if gravity > 0:
        gravity += 1
    else:
        gravity += 1.5
    player_pos[1] += gravity
    player_shape.body.position = player_pos
    space.step(1/60)
    if player_shape.body.velocity.y == 0:
        player_on_ground = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and player_on_ground and not jump_flag:  # added check to see if player is on ground before jumping
            gravity = -15
            jump_flag = True
            player_on_ground = False  # update player on ground status
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            jump_flag = False
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 3
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 3
    # Mise à jour de l'affichage
    screen.fill((0, 0, 0))
    screen.blit(player_image, player_pos)
    screen.blit(ground_image, ground_pos)
    pygame.display.update()
    clock.tick(30)
    player_pos_save = player_pos[1]

# Quitter pygame
pygame.quit()
