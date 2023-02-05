import pygame

from Heroes_Dico import *
from settings import coeff
from random import choice
from copy import deepcopy

class Player():
    def __init__(self, choice, pos, hero):
        self.animations_inventory = hero[0]
        self.data = hero[1]
        self.animations_dico = hero[2]
        self.animation_state = 'Idle'
        self.animation_state_save = 'Walk'

        self.frame_index = 0
        self.animation_speed = 0.15
        self.player_offset = self.data[0]
        self.player_hitbox = self.data[1]
        self.flip_offset = self.data[2]*coeff

        # Player display
        self.rect = pygame.Rect(pos[0], pos[1], self.player_hitbox[0]*coeff , self.player_hitbox[1]*coeff) 
        self.pos = pos
        self.player_on_ground, self.jump_pressed = True, False # to jump only on ground and only once per pression
        if choice == 1:
            self.move_keys = {'jump': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'sprint': pygame.K_LSHIFT}
            self.flip = False
        elif choice == 2:
            self.move_keys = {'jump': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'sprint': pygame.K_RCTRL}
            self.flip = True   

        # player movement
        self.direction= pygame.math.Vector2(0,0)
        self.direction_save = pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 1
        self.jump_speed = -19
        self.effect_timer = 0
        self.effect_duration = -1
        self.effect_ongoing = False
        self.one_more_jump = True
        self.down_movement, self.down_pressed, self.down_movement_allowed = False, False, False
        self.down_movement_timer = 0
        self.down_movement_timer_max = self.player_hitbox[1]*0.07
        self.slide_allowed = False

    def animate(self):
        if self.frame_index == 0 or self.animation_state != self.animation_state_save:
            self.animation = self.animations_inventory[choice(self.animations_dico[self.animation_state])]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
        if self.flip :
            self.image = pygame.transform.flip(self.image, True, False)

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
            if self.player_on_ground :
                self.jump()
            elif self.wall_collision:
                self.wall_jump()
        if not keys[self.move_keys['jump']]:
            self.jump_pressed = False
        
        if keys[self.move_keys['down']]:
            self.gravity = 1.5
            if not self.down_pressed and self.down_movement_allowed:
                self.down_movement_timer = self.down_movement_timer_max
                self.down_pressed = True
        if not keys[self.move_keys['down']]:
            self.gravity = 1
            self.down_pressed = False
    
    def get_animation_state(self):            
        if self.direction.x > 0:
            self.animation_state = 'Walk'
            self.flip = False
        elif self.direction.x < 0:
            self.animation_state = 'Walk'
            self.flip = True
        else:
            self.animation_state = 'Idle'

    def check_animation_change(self):
        if self.direction_save.x != self.direction.x:
            self.frame_index = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.player_on_ground, self.jump_pressed = False, True

    def wall_jump(self):
        self.direction.y = self.jump_speed
        self.wall_collision = False

    def wall_slide(self):
        if self.direction.y > 0 and not(self.player_on_ground) and self.direction.x != 0 and self.slide_allowed:
            self.direction.y = 1

    def check_down_movement(self):
        self.down_movement_timer -= 0.1
        if self.down_movement_timer < 0:
            self.down_movement_timer = 0
        if self.down_movement_timer > 0:
            self.down_movement = True
        else:
            self.down_movement = False
            self.down_movement_allowed = False
            

    def clear_effects(self):
        if self.effect_ongoing:
            self.effect_timer += 0.1
            if int(self.effect_timer) == self.effect_duration:
                self.speed = 4
                self.effect_timer = 0
                self.effect_ongoing = False
    
    def update(self,screen):
        self.get_input()
        self.wall_slide()
        self.check_down_movement()
        self.get_animation_state()
        self.animate()
        self.check_animation_change()

        if self.flip:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff) - self.flip_offset, self.rect.y-(self.player_offset[1]*coeff)))
        else:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff), self.rect.y-(self.player_offset[1]*coeff)))
        self.animation_state_save = self.animation_state
        self.direction_save = deepcopy(self.direction)
        