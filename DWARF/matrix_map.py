import pygame, copy, ctypes, sys
from functions import *
from time import sleep
ctypes.windll.user32.SetProcessDPIAware() # To adapt to screen size

# Initialisation
pygame.init()
# Create the screen
screen = pygame.display.set_mode((1920,1080), pygame.SCALED)
# Taille de la fenêtre
clock = pygame.time.Clock()

# Position initiale du personnage
player_pos = [400, 50]

# Chargement de l'image du personnage
player_image = pygame.image.load("DWARF/icon/icon.png").convert_alpha()
player_image = scale(player_image, 'div', 20)
player_mask = get_mask(player_image)

# Vitesse de déplacement du personnage
player_speed = 3

# Position initiale du sol

# Chargement de l'image du sol
map_matrix = [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
              [3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,3],
              [3,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,3],
              [3,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,3],
              [3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3],
              [3,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,3],
              [3,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,3],
              [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]

# Boucle principale
running = True
player_on_ground = False  # added variable to keep track of player on ground
gravity = 2
mult = 1
jump_flag = False
player_pos_save = copy.deepcopy(player_pos)
while running:
    screen.fill((0, 0, 0))

    y = 0
    for i in range(len(map_matrix)):
        x = 0
        for j in range(len(map_matrix[0])):
            if map_matrix[i][j] == 1:
                if map_matrix[i][j-1] == 1 and map_matrix[i][j+1] == 1 and map_matrix[i-1][j] == 0 and map_matrix[i+1][j] == 1:
                    display_map('Oranges_Rock/UM.png',screen, x, y)
                elif map_matrix[i][j-1] == 1 and map_matrix[i][j+1] == 0 and map_matrix[i-1][j] == 0 and map_matrix[i+1][j] == 1:
                    display_map('Oranges_Rock/UCR.png',screen, x, y)
                elif map_matrix[i][j+1] == 1 and map_matrix[i][j-1] == 0 and map_matrix[i-1][j] == 0 and map_matrix[i+1][j] == 1:
                    display_map('Oranges_Rock/UCL.png',screen, x, y)
                elif map_matrix[i][j+1] == 0 and map_matrix[i][j-1] == 1 and map_matrix[i-1][j] == 1 and map_matrix[i+1][j] == 1:
                    display_map('Oranges_Rock/SR.png',screen, x, y)
                elif map_matrix[i][j-1] == 0 and map_matrix[i][j+1] == 1 and map_matrix[i-1][j] == 1 and map_matrix[i+1][j] == 1:
                    display_map('Oranges_Rock/SL.png',screen, x, y)
                else:
                    display_map('Oranges_Rock/M.png',screen, x, y)
            x += 1
        y += 1
    player_on_ground = False
    if gravity > 0:
        gravity += 0.8
    else:
        gravity += 1.1
    player_pos[1] += gravity

    # Vérification des collisions entre le personnage et le sol

    player_pos_save = copy.deepcopy(player_pos)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_k]:
            pygame.quit()
            sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and player_on_ground and not jump_flag:  # added check to see if player is on ground before jumping
            gravity = -19
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
    screen.blit(player_image, player_pos)
    pygame.display.update()
    clock.tick(60)
    

# Quitter pygame
pygame.quit()