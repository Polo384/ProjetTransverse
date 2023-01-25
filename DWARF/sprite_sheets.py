import pygame
from functions import *
from Heroes_Dico import *

# Initialiser Pygame
pygame.init()

# Initialiser l'écran de jeu
screen = pygame.display.set_mode((800, 600))

all_animations = store_spricesheets([Skeleton])
# Initialiser les variables pour la boucle d'animation
current_frame, current_animation, current_hero = 0, 0, 0
animation_speed = 4
animation_counter = 0

# Boucle principale du jeu
running = True
clock = pygame.time.Clock() 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0,0,0))
    # Afficher le frame courant sur l'écran
    screen.blit(all_animations[0][current_animation][current_frame], (0, 0))
    pygame.display.update()

    # Mettre à jour la boucle d'animation
    animation_counter += 1
    if animation_counter >= animation_speed:
        animation_counter = 0
        current_frame += 1
        if current_frame >= len(all_animations[0][current_animation]):
            current_frame = 0
            current_animation += 1
            if current_animation >= len(all_animations[current_hero]):
                current_animation = 0
                if current_hero >= len(all_animations):
                    current_hero = 0
            
    
    # Limiter les fps
    clock.tick(60)

# Quitter Pygame
pygame.quit()
