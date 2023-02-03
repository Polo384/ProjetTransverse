import pygame

from Heroes_Dico import *
from settings import coeff

class Player():
    def __init__(self, choice, pos, hero):
        self.animations = hero[0]
        hero_data = hero[1]
        self.pos = pos
        self.player_offset = hero_data[0]
        self.player_hitbox = hero_data[1]
        self.jump_check, self.jump_pressed = True, False # to jump only on ground and only once per pression
        if choice == 1:
            self.move_keys = {'jump': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'sprint': pygame.K_LSHIFT}
        elif choice == 2:
            self.move_keys = {'jump': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'sprint': pygame.K_RCTRL}  
        
        # Player display
        self.image = self.animations[0][0]   
        self.rect = pygame.Rect(pos[0], pos[1], self.player_hitbox[0]*coeff , self.player_hitbox[1]*coeff)  

        # player movement
        self.direction= pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 1
        self.jump_speed = -19
        self.effect_timer = 0
        self.effect_duration = -1
        self.effect_ongoing = False
        self.one_more_jump = True

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.move_keys['right']] and keys[self.move_keys['left']]:
            self.direction.x = 0
        elif keys[self.move_keys['right']]:
            self.direction.x = 1
        elif keys[self.move_keys['left']]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[self.move_keys['jump']] and not self.jump_pressed:
            if self.jump_check :
                self.jump()
            elif self.wall_collision:
                self.wall_jump()
        if not keys[self.move_keys['jump']]:
            self.jump_pressed = False
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_check, self.jump_pressed = False, True

    def wall_jump(self):
        self.direction.y = self.jump_speed
        self.wall_collision = False
        #print(f'self.jump_check: {self.jump_check}, self.jump_pressed: {self.wall_jump}, self.wall_collision: {self.wall_collision}')

    def clear_effects(self):
        if self.effect_ongoing:
            self.effect_timer += 0.1
            if int(self.effect_timer) == self.effect_duration:
                self.speed = 4
                self.effect_timer = 0
                self.effect_ongoing = False
    
    def update(self,screen):
        self.get_input()
        screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff), self.rect.y-(self.player_offset[1]*coeff)))
        