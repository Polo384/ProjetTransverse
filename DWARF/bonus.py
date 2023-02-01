import pygame, math, random, sys
from functions import *

pygame.init()

#Fenêtre
pygame.display.set_caption("Icon qui gravite")
screen = pygame.display.set_mode((800, 400))
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("DWARF/bonus_attack.jpg").convert_alpha()
        self.image = scale(self.image, 'mult', 4)
        self.rect = self.image.get_rect()
        self.variable = 0
        self.apparition()

    def apparition(self):
        coordonnees = random.random() #nombre random entre 0 et 1
        #En fonction du nombre qu'on a eu, on fait spawn à trois endroits différents
        if coordonnees<=0.25:
            self.rect.x = 200
            self.rect.y = 50
        elif coordonnees>0.25 and coordonnees<=0.5:
            self.rect.x = 400
            self.rect.y = 100
        else: #plage plus grande ici donc + de probabilité que ça spawn à ces coordonnées
            self.rect.x = 600
            self.rect.y = 200

    def flotter(self):
        self.variable += 0.1
        y = 5*math.sin(self.variable) #réduction du multiplicateur pcq sinon c'est le dawa
        if y < 0:
            self.rect.y -= round(abs(y))
        elif y > 0:
            self.rect.y += round(y)
        else:
            self.variable = 0
           
    def update(self):
        self.flotter()

bonus = Bonus()
bonus.apparition() #tentative d'utilisation de la fonction mais ça n'a eu aucun effet 
bonus_group = pygame.sprite.Group()
bonus_group.add(Bonus())
BONUS = bonus_group.sprites()


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                pygame.quit()
                sys.exit()
    screen.fill((0,0,0))

    bonus_group.update()
    bonus_group.draw(screen)
    pygame.display.update()
    clock.tick(60)