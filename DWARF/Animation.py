import pygame
from functions import store_animations,scale
from Heroes_Dico import heroes_dico, santa_dico_v1, minotaur_dico_v1, dwarf_dico_v1, indiana_jones_dico_v1, adventurer_dico_v1, bat_dico_v1, halo_dico_v1, gladiator_dico_v1, demon_dico_v1, cyclop_dico_v1, hobbit_dico_v2
from settings import coeff
import random

# Dans le main

# Tu passes ça en paramètre pour player


class Player():
    def __init__(self, pos, hero, movement):
        pos = pos
            # Data
        self.mov = movement
        self.animations_inventory = hero[0]
        data = hero[1]
        self.animations_dico = hero[2]
        self.hero_choice = hero[3]
        self.player_offset = data[0]
        self.player_hitbox = data[1]

        # Animation
        self.animations_inventory = hero[0]
        self.animation_state = 'Idle'
        self.animation_state_save = 'Walk'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.selected = 'off'
        
            # Display
        self.rect = pygame.Rect(pos[0], pos[1], self.player_hitbox[0]*coeff , self.player_hitbox[1]*coeff) 
        
        self.rect.x -= self.rect.width/2
        self.rect.y -= self.rect.height/2
        self.pos = (self.rect.x,self.rect.y)
        
    def check_animation_change(self):
        if self.mov == 0:
            self.animation_state = 'Idle'
            self.frame_index = 0
        elif self.mov == 1:
            self.animation_state = 'Walk'
        elif self.mov == 2:
            self.animation_state = 'Attack'
            self.selected = 'running'

    def animate(self):
        if self.frame_index == 0 or self.animation_state != self.animation_state_save:
            self.animation = self.animations_inventory[random.choice(self.animations_dico[self.animation_state])]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.animation):
            self.image = self.animation[len(self.animation)-1]
            self.frame_index = 0
            if self.selected == 'running': self.selected = 'on'
        else:
            self.image = self.animation[int(self.frame_index)]


    def draw_player(self, screen):
        self.image = scale(self.image, 'mult', coeff-0.5)
        screen.blit(self.image, ((self.rect.x-(self.player_offset[0])*(coeff-0.5)*(coeff-0.5)), self.rect.y-(self.player_offset[1]*(coeff-0.5)*(coeff-0.5))))
    def update(self, screen):
        if self.selected != 'on':
            self.check_animation_change()
            self.animate()
        else:
            self.image = self.animations_inventory[random.choice(self.animations_dico['Idle'])][0]

        self.draw_player(screen)
        self.animation_state_save = self.animation_state



