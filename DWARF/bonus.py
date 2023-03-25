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
        self.variable = 0
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
        self.rect.y += round(math.sin(self.variable)*coeff*0.5)
        self.variable += 0.1

    def effect(self, player):
        if self.choice == 'speed':
            player.speed_boost = 1.5
            player.effect_duration = 40
            player.effect_color = (190, 218, 240, 100)

        if self.choice == 'attack':
            player.attack_boost += 0.75
            player.effect_duration = 35
            player.effect_color = (230, 104, 45, 100)

        if self.choice == 'health':
            player.health += 20
            if player.health > player.max_health:
                player.health = player.max_health
            player.effect_duration = 2
            player.effect_color = (134, 203, 61, 150)

        if self.choice == 'resistance':
            player.resistance += 0.75
            player.effect_duration = 45
            player.effect_color = (89, 86, 79, 150)

        if self.choice == 'attack_speed':
            player.attack_speed_boost = 2
            player.effect_duration = 40
            player.effect_color = (48, 179, 174, 150)

        if self.choice in ('minotaur','demon','cyclop'):
            player.start_boss_explosion_animation()
            player.effect_duration = 0


    def update(self):
        self.levitate()