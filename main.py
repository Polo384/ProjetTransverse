import pygame
import math
from classes import * 
pygame.init()


#Fenetre
pygame.display.set_caption("Lalala")
screen = pygame.display.set_mode((1080, 720))


#créer arrière-plan
background = pygame.image.load('PygameAssets-main/bg.jpg')

#importer bannière
banner = pygame.image.load("PygameAssets-main/banner.png")
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x  = math.ceil(screen.get_width() / 4)

#importer le bouton
play_button = pygame.image.load("PygameAssets-main/button.png")
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height()/2)

#Charger le jeu
game = Game()


running = True


#boucle tant que
while running:
    
    #appliquer bg
    screen.blit(background, (0, -200))

    #vérifier si le jeu a commencé
    if game.is_playing:
        #déclencher les instructions du jeu
        game.update(screen)
    #vérifier si le jeu a pas commencé
    else:
        #ajouter écran de bienvenue
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    #mettre a jour ecran
    pygame.display.flip()

    #si le joueur ferme la fenêtre
    for event in pygame.event.get():
        # si l'event est fermeture de la fenêtre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fin")
        #détecter si un joueur press une touche
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            #détecter si espace est enclenché pour lancer projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #verification pour savoir si on clique sur le boutton
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en route
                game.start()