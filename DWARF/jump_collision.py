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
ground_image = pygame.image.load("DWARF/ground.png").convert_alpha()
ground_image = scale(ground_image,'mult',3.5)
ground_pos = [0,408]
ground_mask = get_mask(ground_image)

# Boucle principale
running = True
player_on_ground = False  # added variable to keep track of player on ground
gravity = 2
mult = 1
jump_flag = False
player_pos_save = copy.deepcopy(player_pos)
particles = []
while running:
    screen.fill((0, 0, 0))
    player_on_ground = False
    if gravity > 0:
        gravity += 0.8
    else:
        gravity += 1.1
    player_pos[1] += gravity

    # Vérification des collisions entre le personnage et le sol
    while detect_collision(player_mask, ground_mask, player_pos, ground_pos) and player_pos_save[1]<player_pos[1]:
        gravity = 1
        player_pos[1] -= 1
        player_on_ground = True
    while detect_collision(player_mask, ground_mask, player_pos, ground_pos) and player_pos_save[1]>player_pos[1] and gravity>=0 and not(player_on_ground):
        player_pos[1] += 1
    while detect_collision(player_mask, ground_mask, player_pos, ground_pos) and player_pos_save[0]<player_pos[0] and not(player_pos_save[1]<player_pos[1]):
        player_pos[0] -= 1
    while detect_collision(player_mask, ground_mask, player_pos, ground_pos) and player_pos_save[0]>player_pos[0]:
        player_pos[0] += 1

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
        particles.append([[copy.deepcopy(player_pos[0]), copy.deepcopy(player_pos[1])], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

    # Mise à jour de l'affichage
    screen.blit(player_image, player_pos)
    screen.blit(ground_image, ground_pos)
    pygame.display.update()
    clock.tick(60)
    

# Quitter pygame
pygame.quit()