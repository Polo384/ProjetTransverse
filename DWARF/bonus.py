import pygame, math, random
from functions import *
from settings import coeff
clock = pygame.time.Clock()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, choice):
        super().__init__()
        self.choice = choice
        self.image = pygame.image.load('DWARF/Bonus/bonus_'+self.choice+'.png').convert_alpha()
        self.image = scale(self.image, 'mult', coeff)
        self.rect = self.image.get_rect()
        self.variable = 1
        self.apparition()
        
    def apparition(self):
        coordonnees = random.random() #nombre random entre 0 et 1
        #En fonction du nombre qu'on a eu, on fait spawn à trois endroits différents
        if coordonnees<=0.25:
            self.rect.x = 100*coeff
            self.rect.y = 70*coeff
        elif coordonnees>0.25 and coordonnees<=0.5:
            self.rect.x = 200*coeff
            self.rect.y = 60*coeff
        else: #plage plus grande ici donc + de probabilité que ça spawn à ces coordonnées
            self.rect.x = 300*coeff
            self.rect.y = 100*coeff

    def levitate(self):
        self.variable += 0.14
        y = coeff*0.8*math.sin(self.variable) #réduction du multiplicateur pcq sinon c'est le dawa
        if y < 0:
            self.rect.y += round(y)
            
        elif y > 0:
            self.rect.y += round(y)
        else:
            self.variable = 0

    def effect(self, player):
        if self.choice == 'speed':
            player.speed *= 2
            player.effect_duration = 30
        if self.choice == 'attack':
            player.effect_duration = 10
        if self.choice == 'health':
            player.effect_duration = 25

    def update(self):
        self.levitate()