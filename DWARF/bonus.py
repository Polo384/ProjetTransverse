import pygame, math, random
from functions import *
from settings import coeff, tile_size
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
        coordonnees = random.randint(1, 9) #nombre random 
        #En fonction du nombre qu'on a eu, on fait spawn à trois endroits différents
        
        if coordonnees==1:
            self.rect.x = tile_size*coeff*13.7 - tile_size*coeff
            self.rect.y = tile_size*coeff*6.5 - tile_size*coeff
        elif coordonnees==2:
            self.rect.x = tile_size*coeff*13.25 - tile_size*coeff
            self.rect.y = tile_size*coeff*15.4 - tile_size*coeff
        elif coordonnees==3:
            self.rect.x = tile_size*coeff*3.4 - tile_size*coeff 
            self.rect.y = tile_size*coeff*16.5 - tile_size*coeff
        elif coordonnees==4:
            self.rect.x = tile_size*coeff*35 - tile_size*coeff
            self.rect.y = tile_size*coeff*5.3 - tile_size*coeff
        elif coordonnees==5:
            self.rect.x = tile_size*coeff*3 - tile_size*coeff
            self.rect.y = tile_size*coeff*6 - tile_size*coeff
        elif coordonnees==6:
            self.rect.x = tile_size*coeff*23.5 - tile_size*coeff
            self.rect.y = tile_size*coeff*5.5 - tile_size*coeff
        elif coordonnees==7:
            self.rect.x = tile_size*coeff*27.8 - tile_size*coeff
            self.rect.y = tile_size*coeff*10.3 - tile_size*coeff
        elif coordonnees==8:
            self.rect.x = tile_size*coeff*21 - tile_size*coeff
            self.rect.y = tile_size*coeff*19.3 - tile_size*coeff
        else:
            self.rect.x = tile_size*coeff*32 - tile_size*coeff
            self.rect.y = tile_size*coeff*16.5 - tile_size*coeff

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
            player.effect_duration = 50
            player.effect_color = (230, 104, 45, 100)

        if self.choice == 'health':
            player.health += 20
            if player.health > player.max_health:
                player.health = player.max_health
            player.effect_duration = 1
            player.effect_color = (134, 203, 61, 150)

        if self.choice == 'resistance':
            player.resistance += 0.75
            player.effect_duration = 60
            player.effect_color = (89, 86, 79, 150)

        if self.choice == 'attack_speed':
            player.attack_speed_boost = 2
            player.effect_duration = 50
            player.effect_color = (48, 179, 174, 150)

        if self.choice in ('minotaur','demon','cyclop'):
            player.start_boss_explosion_animation()
            player.effect_duration = 0


    def update(self):
        self.levitate()