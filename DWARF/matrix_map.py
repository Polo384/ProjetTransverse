import pygame, copy, ctypes, sys, random
from functions import *
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
# 1 = rock/ 2 = bridge/ 3 = frame/ 4 = grass/ 5 = stone
map =        [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
              [3,0,0,0,0,0,5,0,4,4,4,4,4,0,0,0,0,0,0,0,0,3],
              [3,0,0,0,0,1,1,1,1,1,1,1,2,0,0,0,4,4,1,1,1,3],
              [3,0,0,0,0,1,1,1,1,1,1,1,0,0,0,2,2,1,1,1,1,3],
              [3,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,3],
              [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,3],
              [3,5,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,2,0,0,0,0,0,0,0,0,4,4,4,4,0,5,0,0,1,3],
              [3,1,1,0,0,0,0,0,0,5,0,0,2,2,2,2,2,2,0,0,1,3],
              [3,1,1,4,4,5,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,3],
              [3,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,3],
              [3,1,1,1,1,1,1,0,1,1,5,0,0,0,0,0,0,0,0,4,4,3],
              [3,1,1,1,1,1,1,1,1,1,1,1,0,0,0,4,4,4,4,1,1,3],
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


# =========== MAP ADDONS ===========
stone_list = []
stone_occurrences = element_occurrences(map, 5)
for temp in range(stone_occurrences):
    stone_list.append(str(random.randint(1,6)))

grass_list = []
grass_occurrences = element_occurrences(map, 4)
for temp in range(grass_occurrences):
    grass_list.append((random.choice(['F','G1','G1','G1'])))

water_level = 3
ground_level = 4
# ==================================

while running:
    screen.fill((20, 200,200))

# ============= MAP ================
    stone_index, grass_index = 0, 0
    y = 0
    for i in range(len(map)):
        x = 0
        for j in range(len(map[0])):

            if  y == (len(map)-water_level)  and  y != (len(map)-1):
                display_map('Water/W1.png',screen, x, y)
            elif y > (len(map)-water_level)  and  y != (len(map)-1):
                display_map('Water/W2.png',screen, x, y)

            if map[i][j] == 1: # Collisions Blocks                    
                # Yellow Blocks
                if (map[i][j-1] == 1 or map[i][j-1] == 3) and (map[i][j+1] == 1 or map[i][j+1] == 3) and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 1:
                    display_map('Yellow_Rock_Block/UM.png',screen, x, y)
                    

                elif map[i][j+1] != 1 and map[i][j-1] == 1 and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 1:
                    if map[i][j+1] == 2:
                        display_map('Yellow_Rock_Block/UM.png',screen, x, y)
                        display_map('Yellow_Rock_Block/UCR+.png',screen, x, y)
                    else:
                        display_map('Yellow_Rock_Block/UCR.png',screen, x, y)

                elif map[i][j+1] == 1 and map[i][j-1] != 1 and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 1:
                    if map[i][j-1] == 2:
                        display_map('Yellow_Rock_Block/UM.png',screen, x, y)
                        display_map('Yellow_Rock_Block/UCL+.png',screen, x, y)
                    else:
                        display_map('Yellow_Rock_Block/UCL.png',screen, x, y)

                elif (map[i][j+1] == 0 or map[i][j+1] == 5 or map[i][j+1] == 4) and map[i][j-1] == 1 and map[i-1][j] == 1 and (map[i+1][j] == 1 or map[i+1][j] == 3):
                    if map[i-2][j] == 0 or map[i-2][j] == 4 or map[i-2][j] == 5:
                        display_map('Purple_Rock_Yellow_Rock/R.png',screen, x, y)
                    else:
                        display_map('Purple_Rock_Ground/R.png',screen, x, y)

                elif map[i][j+1] == 1 and map[i][j-1] == 0 and map[i-1][j] == 1 and (map[i+1][j] == 1 or map[i+1][j] == 3):
                    if map[i-2][j] == 0 or map[i-2][j] == 4 or map[i-2][j] == 5:
                        display_map('Purple_Rock_Yellow_Rock/L.png',screen, x, y)
                    else:
                        display_map('Purple_Rock_Ground/L.png',screen, x, y)
                        
                elif if_matrix(map, i, j,1,1,1,1) and map[i-1][j-1] == 1 and (map[i-1][j+1] == 0 or map[i-1][j+1] == 4 or map[i-1][j+1] == 5):
                    display_map('Yellow_Rock_Block/L.png',screen, x, y)

                elif if_matrix(map, i, j,1,1,1,1) and map[i-1][j+1] == 1 and (map[i-1][j-1] == 0 or map[i-1][j-1] == 4 or map[i-1][j-1] == 5):
                    display_map('Yellow_Rock_Block/R.png',screen, x, y)


                # Purple ks
                elif (map[i][j+1] == 1 or map[i][j+1] == 3) and map[i][j-1] == 1 and map[i-1][j] == 1 and map[i+1][j] == 1 and map[i+1][j-1] == 0:
                    display_map('Purple_Rock_Round_Bottom_Bottom/L.png',screen, x, y)

                elif (map[i][j-1] == 1 or map[i][j-1] == 3) and map[i][j+1] == 1 and map[i-1][j] == 1 and map[i+1][j] == 1 and map[i+1][j+1] == 0:
                    display_map('Purple_Rock_Round_Bottom_Bottom/L.png',screen, x, y)

                elif if_matrix(map, i, j,1,1,1,0):
                    display_map('Purple_Rock_Round_Top_Top/M.png',screen, x, y)

                elif (map[i][j-1] == 1 or map[i][j-1] == 3) and map[i][j+1] == 0 and map[i-1][j] == 1 and map[i+1][j] == 0:
                    display_map('Purple_Rock_Round_Top_Top/R.png',screen, x, y)

                elif (map[i][j+1] == 1 or map[i][j+1] == 3) and map[i][j-1] == 0 and map[i-1][j] == 1 and map[i+1][j] == 0:
                    display_map('Purple_Rock_Round_Top_Top/L.png',screen, x, y)

                elif if_matrix(map, i, j,3,0,1,1):
                    display_map('Purple_Rock_Ground/L.png',screen, x, y)

                elif if_matrix(map, i, j,3,0,0,1):
                    display_map('Purple_Rock_Round_Top_Top/R2.png',screen, x, y)

                # Classic
                else:
                    display_map('Yellow_Rock_Block/M.png',screen, x, y)


            elif map[i][j] == 2: # one-way collision blocks
                # Bridges
                if (map[i][j+1] == 2 or map[i][j+1] == 1) and (map[i][j-1] == 2 or map[i][j-1] == 1) and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 0:
                    display_map('Bridge/M.png',screen, x, y)

                elif (map[i][j+1] == 2 or map[i][j+1] == 1) and map[i][j-1] == 0 and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 0:
                    display_map('Bridge/L.png',screen, x, y)

                elif map[i][j+1] == 0 and (map[i][j-1] == 2 or map[i][j-1] == 1) and (map[i-1][j] == 0 or map[i-1][j] == 5 or map[i-1][j] == 4) and map[i+1][j] == 0:
                    display_map('Bridge/R.png',screen, x, y)


            elif map[i][j] == 4 or map[i][j] == 5:# No collision Blocks
                # Grass
                if map[i][j] == 4:
                    if map[i][j-1] == 4 and map[i][j+1] != 4:
                        screen.blit(scale(pygame.image.load('DWARF/Tiles/Grass/RC.png').convert_alpha(),'mult',2),(x*17*2-17*2,y*17*2-17*2+4))
                    elif map[i][j-1] !=4 and map[i][j+1] == 4:
                        screen.blit(scale(pygame.image.load('DWARF/Tiles/Grass/LC.png').convert_alpha(),'mult',2),(x*17*2-17*2,y*17*2-17*2+4))
                    else:
                        screen.blit(scale(pygame.image.load('DWARF/Tiles/Grass/'+grass_list[grass_index]+'.png').convert_alpha(),'mult',2),(x*17*2-17*2,y*17*2-17*2+4))
                    # Didn't use the function in order to add +5 to the y position, else the stone were levitating from a couple of pixels
                    if grass_index < grass_occurrences:
                        grass_index += 1
                    else:
                        grass_index = 0

                # Stones
                elif map[i][j] == 5:
                    screen.blit(scale(pygame.image.load('DWARF/Tiles/Stone/S'+str(stone_list[stone_index])+'.png').convert_alpha(),'mult',2),(x*17*2-17*2,y*17*2-17*2+4))
                    # Didn't use the function in order to add +5 to the y position, else the stone were levitating from a couple of pixels
                    if stone_index < stone_occurrences:
                        stone_index += 1
                    else:
                        stone_index = 0
            x += 1
        y += 1
# ==================================
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