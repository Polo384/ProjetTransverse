import pygame
import random

#créer classe pour gérer l'event
class CometFallEvent:

    #lors du chargement -> créer compteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 10
        self.game = game
        self.fall_mode = False

        #définir groupe de sprite pour stocker les comètes
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed/100

    def is_full_loaded(self):
        return self.percent >= 100
    
    def reset_percent(self):
        self.percent = 0
    
    def meteor_fall(self):
        for i in range(random.randint(1, 10)):
            self.all_comets.add(Comet(self))
        
    def attempt_fall(self):
        #si la jauge est chargé
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            print("Pluie de comètes")
            self.meteor_fall()
            self.fall_mode = True #Activer l'event

    def update_bar(self, surface):
        #ajouter du pourcentage
        self.add_percent()

        #barre d'arrière plan
        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height()-20, surface.get_width(), 10])
        #barre premier plan (la jauge qui monte)
        pygame.draw.rect(surface, (187, 11, 11), [0, surface.get_height()-20, (surface.get_width()/100)*self.percent, 10])

#classe pour gérer la comète
class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event):
        super().__init__()
        #définir l'image de la comète
        self.image = pygame.image.load("PygameAssets-main/comet.png")
        self.rect = self.image.get_rect()
        self.velocity = 1+random.random()
        self.rect.x = random.randint(20, 800)
        self.rect.y = -random.randint(0, 800)
        self.comet_event = comet_event

    def remove(self):
            self.comet_event.all_comets.remove(self)

            #vérifier si il reste des comètes
            if len(self.comet_event.all_comets) == 0:
                self.comet_event.reset_percent()
                self.comet_event.game.spawn_monster()
                self.comet_event.game.spawn_monster()
    
    def fall(self):
        self.rect.y += self.velocity

        #ne tombe pas sur le sol
        if self.rect.y >= 525:
            self.remove()
            #verifier si il reste des boules sur le jeu
            if len(self.comet_event.all_comets) == 0:
                print("Event fini")
                #remettre jauge au départ
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False
        #vérifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print("Joueur touché")
            #retirer boule de feu
            self.remove()
            #subier des dégats
            self.comet_event.game.player.dammage(20)