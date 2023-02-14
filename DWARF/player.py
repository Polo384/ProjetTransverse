import pygame
from time import sleep
from Heroes_Dico import *
from settings import coeff
from random import choice
from copy import deepcopy
from functions import store_dust_animations

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

        # Dust animation
        self.dust_animations = store_dust_animations([[3], [6,5,5]])
        self.dust_animation_state = 'Run'
        self.dust_animation_state_save = 'Land'
        self.dust_frame_index = 0
        self.dust_animations_dico = {'Jump':0, 'Land':1, 'Run':2}
        self.dust_animation_running = False
        self.dust_image = self.dust_animations[0][0]
        self.jump_dust_coordonates = (0,0)
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
        self.speed = coeff
        self.speed_boost = 1
        self.stamina = 10
        self.sprinting, self.sprint_allowed, self.moving_pressed, self.sprint_release = False, False, False, False
        self.sprint_timer, self.sprint_release_timer = 0, 0
        self.gravity = coeff/4
        self.jump_speed = -4.75*coeff
        self.effect_timer = 0
        self.effect_duration = -1
        self.effect_ongoing = False
        self.one_more_jump = True
        self.down_movement, self.down_pressed, self.down_movement_allowed = False, False, False
        self.down_movement_timer = 0
        self.down_movement_timer_max = self.player_hitbox[1]*0.09
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
        self.keys = pygame.key.get_pressed()

        if self.keys[self.move_keys['right']] and self.keys[self.move_keys['left']]:
            self.direction.x = 0
        elif self.keys[self.move_keys['right']]:
            self.direction.x = 1
        elif self.keys[self.move_keys['left']]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if self.keys[self.move_keys['jump']] and not self.jump_pressed:
            if self.player_on_ground :
                self.jump()
            elif self.wall_collision:
                self.wall_jump()
        if not self.keys[self.move_keys['jump']]:
            self.jump_pressed = False
        
        if self.keys[self.move_keys['down']]:
            if not self.down_movement_allowed:
                self.gravity = coeff/2
            if not self.down_pressed and self.down_movement_allowed:
                self.down_movement_timer = self.down_movement_timer_max
                self.down_pressed = True
        if not self.keys[self.move_keys['down']]:
            self.gravity = coeff/4
            self.down_pressed = False

    def reload_stamina(self):
        if self.stamina < 10:
            self.stamina += 0.03
    
    def use_stamina(self):
        if self.stamina > 0:
            self.stamina -= 0.04
    
    def check_if_sprinting(self):
        keys = pygame.key.get_pressed()
        moving_right = keys[self.move_keys['right']]
        moving_left = keys[self.move_keys['left']]

        if moving_right or moving_left:

            # 5 : pressed
            if not self.moving_pressed and self.sprint_release:
                self.sprint_release = False
                self.sprint_release_timer = 0
                self.moving_pressed = True
                self.sprinting = True
                
            # 3 : pressed
            elif not self.moving_pressed and self.sprint_allowed:
                self.moving_pressed = True
                self.sprinting = True
                self.sprint_allowed = False
                
            # 1 : pressed
            elif not self.moving_pressed:
                self.moving_pressed = True
                self.sprint_timer = 0
                self.sprint_allowed = True
        else:
            # 4 : released
            if self.moving_pressed and self.sprinting:
                self.moving_pressed = False
                self.sprint_release = True
            
            # 2 : released
            elif self.moving_pressed:
                self.moving_pressed = False
                self.sprint_timer = 0

        # 1
        if self.sprint_allowed:
            self.sprint_timer += 0.1
            if self.sprint_timer > 2:
                self.sprint_timer = 0
                self.sprint_allowed = False
        
        # 4
        if self.sprint_release:
            self.sprint_release_timer += 0.1
            if self.sprint_release_timer > 1.2:
                self.sprinting = False
                self.sprint_release_timer = 0
                self.sprint_release = False
                
    def sprint(self):
        self.check_if_sprinting()

        if self.sprinting and self.direction.x != 0:
            if self.stamina > 0.1:
                self.speed = coeff*1.5
                self.use_stamina()
            elif self.stamina <= 0.1:
                self.use_stamina()
                self.speed = coeff
        else:
            self.sprinting = False
            self.speed = coeff
            self.reload_stamina()

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

    def animate_dust(self, state):
        if self.dust_frame_index == 0 or self.dust_animation_state != self.dust_animation_state_save:
            self.dust_animation = self.dust_animations[self.dust_animations_dico[state]]
        self.dust_frame_index += self.animation_speed

        if self.dust_frame_index >= len(self.dust_animation):
            self.dust_frame_index = 0
        
        self.dust_image = self.dust_animation[int(self.dust_frame_index)]

        if self.dust_frame_index >= len(self.dust_animation)-2:  # in order to not have another frame on the jump animation
            self.dust_animation_running = False
            self.dust_frame_index = 0

        return self.dust_animation_running

    def update_dust_animation(self,screen):
        if self.speed != coeff and self.player_on_ground:
            width = 14*coeff
            height = 10*coeff
            self.animate_dust('Run')
            if self.flip :
                self.dust_image = pygame.transform.flip(self.dust_image, True, False)
                screen.blit(self.dust_image, (self.rect.x+self.player_hitbox[0]*coeff, self.rect.y+self.player_hitbox[1]*coeff-height))
            else:
                screen.blit(self.dust_image, (self.rect.x-width, self.rect.y+self.player_hitbox[1]*coeff-height))
        
        elif (self.direction.y < 0 and (self.direction_save.y == 0 or self.direction_save.y == 0.5) ) or (self.dust_animation_running):
            width = 34*coeff
            height = 32*coeff
            self.dust_animation_running = True
            if self.direction.y < 0 and (self.direction_save.y == 0 or self.direction_save.y == 0.5):
                self.jump_dust_coordonates = (self.rect.x - abs(width-self.player_hitbox[0]*coeff)/2, self.rect.y+self.player_hitbox[1]*coeff-height)
                self.dust_frame_index = 0

            self.dust_animation_running = self.animate_dust('Jump')
            screen.blit(self.dust_image, self.jump_dust_coordonates)
    
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
                self.speed_boost = 1
                self.effect_timer = 0
                self.effect_ongoing = False
    
    def update(self,screen):
        self.get_input()
        self.sprint()
        self.wall_slide()
        self.check_down_movement()
        self.get_animation_state()
        self.animate()
        self.check_animation_change()
        self.update_dust_animation(screen)
        
        #screen.blit(pygame.Surface((self.rect.width,self.rect.height)),self.rect)

        if self.flip:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff) - self.flip_offset, self.rect.y-(self.player_offset[1]*coeff)))
        else:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff), self.rect.y-(self.player_offset[1]*coeff)))
            
        # saves
        self.animation_state_save, self.dust_animation_state_save = self.animation_state, self.dust_animation_state
        self.direction_save = deepcopy(self.direction)

        # stamina
        stamina_surface = pygame.Surface((self.stamina*5,10))
        stamina_surface.fill('Red')
        screen.blit(stamina_surface,(self.rect.x,self.rect.y-20))