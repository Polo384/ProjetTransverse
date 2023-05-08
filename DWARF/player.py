import pygame
from Heroes_Dico import *
from settings import coeff, max_map_width, max_map_height
import random
from copy import deepcopy
from functions import store_special_animations, scale
import sys
from projectilesclass import Shell, Grenade
import math

# Didn't do a sprite class because rectangle doesn't correspond to the image (there are alpha pixels)
class Player():
    def __init__(self, choice, pos, hero):
        self.check_invincible = False
        self.choice = choice
        
    # Store heroe data
        self.animations_inventory = hero[0]
        self.data = hero[1]
        self.animations_dico = hero[2]
        self.hero_choice = hero[3]
        self.player_offset = self.data[0]
        self.player_hitbox = self.data[1]
        self.flip_offset = self.data[2]*coeff
        all_stats = hero[4]

    # Initialize player animation
        self.animation_state = 'Idle'
        self.animation_state_save = 'Walk'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.special_animation = False

    # Initialize dust animation
        self.dust_animations = store_special_animations([[3], [6,5,5]], 'Dust_particles')
        self.dust_animation_state = 'Run'
        self.dust_animation_state_save = 'Land'
        self.dust_frame_index = 0
        self.dust_animations_dico = {'Jump':0, 'Land':1, 'Run':2}
        self.dust_animation_running = False
        self.dust_image = self.dust_animations[0][0]
        self.jump_dust_coordonates = (0,0)
        self.dust_animation_allow = False


    # Player display
        self.rect = pygame.Rect(pos[0], pos[1], self.player_hitbox[0]*coeff , self.player_hitbox[1]*coeff) 
        self.pos = pos
        self.player_on_ground, self.jump_pressed = True, False # to jump only on ground and only once per pression
    
    # Player input
        if choice == 1:
            self.input_keys = {'jump': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'attack': pygame.K_f, 'shoot': pygame.K_g, 'change_weapon': pygame.K_e}
            self.flip = False
        elif choice == 2:
            self.input_keys = {'jump': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'attack': pygame.K_o, 'shoot': pygame.K_m, 'change_weapon': pygame.K_p}
            self.flip = True   

    # Player shooting
        self.angle = 0
        self.time_pressed = 0
        self.shoot = False 
        self.time = 0
        self.shoot_pressed = False
        self.shoot_allowed, self.shoot_allowed_save = False, False
        self.shoot_timer_incrementation = False
        self.shoot_timer = 35
        self.max_shoot_timer = 30
        self.shell, self.grenade = None, None
        self.grenade_timer = 0
        self.current_weapon = True # True means shell and False means grenade

    # Player movement

        # Default movement
        self.direction= pygame.math.Vector2(0,0)
        self.direction_save = pygame.math.Vector2(0,0)
        self.default_speed = all_stats['speed']
        self.speed = self.default_speed
        self.speed_fix_timer = all_stats['speed_fix']
        self.speed_boost = 1
        self.max_stamina = all_stats['stamina']
        self.stamina = self.max_stamina
        self.gravity = coeff/4
        self.jump_speed = -4.75*coeff
        self.freezed = False
        self.moving_left, self.moving_right, self.moving_up, self.moving_down = False, False, False, False
        self.speed_fix_variable = 0
        self.speed_fix_check = False

        # Sprint
        self.sprinting, self.sprint_allowed, self.moving_pressed, self.sprint_release = False, False, False, False
        self.sprint_timer, self.sprint_release_timer = 0, 0

        # Double jump (most of it in Level class)
        self.one_more_jump = True
        self.slide_allowed = False

        # Down movement (higher gravity / passing through plateforms)
        self.down_movement, self.down_pressed, self.down_movement_allowed = False, False, False
        self.down_movement_timer = 0
        # Change down_movement_timer_max because it depends on the size of the heroe. Taller heroe ==> higher down_movement_timer_max,
        # but it can vary because the gravitry is not increasing linearly.
        if self.hero_choice == 'minotaur' or self.hero_choice == 'cyclop':
            self.down_movement_timer_max = self.player_hitbox[1]*0.07
        elif self.hero_choice == 'santa':
            self.down_movement_timer_max = self.player_hitbox[1]*0.08
        elif self.hero_choice == 'demon' or self.hero_choice == 'bat':
            self.down_movement_timer_max = 0
        elif self.hero_choice == 'hobbit':
            self.down_movement_timer_max = self.player_hitbox[1]*0.12
        else:
            self.down_movement_timer_max = self.player_hitbox[1]*0.09

    # Player health
        self.max_health = all_stats['health']
        self.health = self.max_health
        self.temp_invincibility = False
        self.dead = False
        self.death_animation_stop = False
        self.resistance = 1
        self.regeneration_timer = 75

    # Player attack
        self.attack_rect_width, self.attack_rect_height = self.data[3]*coeff, self.player_hitbox[1]*coeff
        self.attack_rect = pygame.Rect(-500,-100, self.attack_rect_width, self.attack_rect_height)
        self.attack = all_stats['attack']
        self.attack_boost = 1
        self.push = 0
        self.opponent_flip = self.flip
        self.attack_pressed = False
        self.attack_timer = 0
        self.attack_speed = all_stats['attack_speed']
        self.attack_speed_boost = 1

    # Effect
        self.effect_timer = 0
        self.effect_duration = -1
        self.effect_ongoing = False  
        self.effect_color = (0,0,0,0)
    
    # Boss explosion
        self.boss_explosion_animations = store_special_animations([[1], [8]], 'Explosion')
        self.boss_explosion_frame_index = 0
        self.boss_explosion_animation_running = False
        self.boss_explosion_image = self.boss_explosion_animations[0][0]
        self.jump_boss_explosion_coordonates = (0,0)
        self.boss_explosion_animation_allow = False


    def animate(self):
        if self.frame_index == 0 or self.animation_state != self.animation_state_save:
            self.animation = self.animations_inventory[random.choice(self.animations_dico[self.animation_state])]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.image = self.animation[len(self.animation)-1]
            self.frame_index = 0
            self.special_animation = False
            if self.dead : self.death_animation_stop = True
        else:
            self.image = self.animation[int(self.frame_index)]
        if self.flip :
            self.image = pygame.transform.flip(self.image, True, False)

    def get_input(self):
        keys = pygame.key.get_pressed()
    # Move
        if self.moving_right:
            self.direction.x = 1
        elif self.moving_left:
            self.direction.x = -1
        else:
            self.direction.x = 0

    # Jump
        if self.moving_up and not self.jump_pressed:
            if self.player_on_ground :
                self.jump()
            elif self.wall_collision:
                self.wall_jump()
        if not self.moving_up:
            self.jump_pressed = False
        
    # Fall
        if self.moving_down:
            if not self.down_movement_allowed:
                self.gravity = coeff/2
            else:
                self.gravity = coeff/4
            if not self.down_pressed and self.down_movement_allowed:
                self.down_movement_timer = self.down_movement_timer_max
                self.down_pressed = True
        if not self.moving_down:
            self.gravity = coeff/4
            self.down_pressed = False
        
    
    def speed_fix(self):
        if self.speed <= 10:
            self.speed_fix_variable += 1
            if self.speed_fix_variable > self.speed_fix_timer:
                self.speed_fix_variable = 0
            
            
            if self.speed_fix_variable == 1:
                self.speed_fix_check = True
            else:
                self.speed_fix_check = False
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_h):
                pygame.quit()
                sys.exit()

            if not self.dead:
                if event.type == pygame.KEYDOWN:
                    if event.key == self.input_keys['attack']:
                        self.attack_pressed = True
                    elif event.key == self.input_keys['shoot'] and not self.shoot_timer_incrementation:
                        self.shoot_pressed = True
                        self.shoot_allowed = True
                        if self.flip:
                            self.angle = 180
                        else:
                            self.angle = 0
                    elif event.key == self.input_keys['change_weapon']:
                        self.current_weapon = not self.current_weapon

                    if event.key == self.input_keys['left']:
                        self.moving_left = True
                    elif event.key == self.input_keys['right']:
                        self.moving_right = True
                    if event.key == self.input_keys['jump']:
                        self.moving_up = True
                    elif event.key == self.input_keys['down']:
                        self.moving_down = True
                        

                if event.type == pygame.KEYUP:
                    if event.key == self.input_keys['attack']:
                        self.attack_pressed = False
                    elif event.key == self.input_keys['shoot']:
                        self.shoot_pressed = False
                        self.shoot_allowed = False
                    if event.key == self.input_keys['left']:
                        self.moving_left = False
                    elif event.key == self.input_keys['right']:
                        self.moving_right = False
                    if event.key == self.input_keys['jump']:
                        self.moving_up = False
                    elif event.key == self.input_keys['down']:
                        self.moving_down = False
            

    def check_attack_input(self):
        # Attack
        if self.attack_pressed and self.attack_timer <= 0:
            self.fighting()
            self.check_invincible = random.choice([True,True,False])
            self.attack_timer = 600/(self.attack_speed*self.attack_speed_boost)
        elif not self.attack_pressed:
            self.attack_rect.x = -500
            if self.attack_timer > 0:
                self.update_attack_timer()
        else:
            self.attack_rect.x = -500
    
    def check_shoot_input(self):
        if self.shoot_pressed and self.shoot_allowed :
            self.freeze()
            self.attack_timer = 2
            self.check_change_orientation()
            self.incline_cursor()
            self.cursorx = int(self.rect.centerx + 30*coeff * math.cos(math.radians(self.angle)))
            self.cursory = int(self.rect.centery + 30*coeff * math.sin(math.radians(self.angle)))

        if self.shoot_allowed_save and not self.shoot_pressed and self.shoot_timer>=self.max_shoot_timer:
            if self.current_weapon:
                self.shell = Shell(self.rect.centerx, self.rect.centery, -self.angle, self.choice, self.flip)
            else:
                self.grenade = Grenade(self.rect.centerx, self.rect.centery, self.cursorx, self.cursory, self.choice, self.flip)
            self.shoot_timer = 0
            self.shoot_timer_incrementation = True
            self.unfreeze()
            self.shoot_allowed = False

        elif self.attack_pressed and self.shoot_allowed_save:
            self.unfreeze()
            self.shoot_alloswed = False
    
    def shoot_timer_update(self):
        if self.shoot_timer_incrementation:
            self.shoot_timer+=0.1
        if int(self.shoot_timer) >= int(self.max_shoot_timer):
            self.shoot_timer_incrementation = False
            
    def check_change_orientation(self):
        if self.moving_left and not self.flip:
            self.flip = not self.flip
            self.angle = 180
        elif self.moving_right and self.flip:
            self.flip = not self.flip
            self.angle = 0

    def incline_cursor(self):
        if not self.flip:
            if self.moving_up and self.angle > -85:
                self.angle -= 3.5
            elif self.moving_down and self.angle < 85:
                self.angle += 3.5
        else:
            if self.moving_down and self.angle > 95:
                self.angle -= 3.5
            elif self.moving_up and self.angle < 265:
                self.angle += 3.5
    
    def draw_cursor(self, screen):
        if self.shoot_pressed and self.shoot_allowed:
            pygame.draw.circle(screen, (47, 47, 46), (self.cursorx, self.cursory), 7)
            pygame.draw.circle(screen, (255, 255, 255), (self.cursorx, self.cursory), 4)

    def grenade_countdown(self):
        if self.grenade:
            self.grenade_timer += 0.1

    def explode_grenade(self):
        self.grenade = None
        self.grenade_timer = 0

    def explode_shell(self):
        self.shell = 0

    def attack_rect_update(self):
        self.attack_rect.x = -500
        if self.attack_timer > 0:
            self.update_attack_timer()

    def freeze(self):
        self.direction.x = 0
        if self.direction.y < 0:
            self.direction.y = 0
        self.down_movement = False
        self.freezed = True

    def unfreeze(self):
        self.freezed = False

    def invincible(self):
        self.temp_invincibility = True
    def not_invincible(self):
        self.temp_invincibility = False

    def update_attack_timer(self):
        self.attack_timer -= 0.5
        if self.attack_timer <= 0:
            self.attack_timer = 0

    def reload_stamina(self):
        if self.stamina < self.max_stamina:
            self.stamina += 0.3*self.speed_boost

    def use_stamina(self):
        if self.stamina > 1:
            self.stamina -= 0.4/self.speed_boost

    def check_if_sprinting(self):
        if self.moving_right or self.moving_left:

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
            if self.stamina > 1:
                self.speed = self.default_speed*1.5
                self.use_stamina()
            elif self.stamina <= 1:
                self.use_stamina()
                self.speed = self.default_speed
        else:
            self.sprinting = False
            self.speed = self.default_speed
            self.reload_stamina()

    def get_animation_state(self):   
        if not self.special_animation:  
            if self.direction.x > 0:
                self.animation_state = 'Walk'
                self.flip = False
            elif self.direction.x < 0:
                self.animation_state = 'Walk'
                self.flip = True
            else:
                self.animation_state = 'Idle'

    def check_animation_change(self):
        if self.direction_save.x != self.direction.x and not self.special_animation:
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

    def update_dust_animation_allow(self):
        self.dust_animation_allow = self.player_on_ground

    def update_dust_animation(self,screen):
        if self.speed != self.default_speed*self.speed_boost and self.player_on_ground:
            width = 14*coeff
            height = 10*coeff
            self.animate_dust('Run')
            if self.flip :
                self.dust_image = pygame.transform.flip(self.dust_image, True, False)
                screen.blit(self.dust_image, (self.rect.x+self.player_hitbox[0]*coeff, self.rect.y+self.player_hitbox[1]*coeff-height))
            else:
                screen.blit(self.dust_image, (self.rect.x-width, self.rect.y+self.player_hitbox[1]*coeff-height))
        
        elif self.dust_animation_allow and (self.direction.y < 0 and (self.direction_save.y == 0 or self.direction_save.y == 0.5) ) or (self.dust_animation_running):
            width = 34*coeff
            height = 32*coeff
            self.dust_animation_running = True
            if self.direction.y < 0 and (self.direction_save.y == 0 or self.direction_save.y == 0.5):
                self.jump_dust_coordonates = (self.rect.x - abs(width-self.player_hitbox[0]*coeff)/2, self.rect.y+self.player_hitbox[1]*coeff-height)
                self.dust_frame_index = 0

            self.dust_animation_running = self.animate_dust('Jump')
            screen.blit(self.dust_image, self.jump_dust_coordonates)


    def start_boss_explosion_animation(self):
        self.boss_explosion_animation_running = True
        self.boss_explosion_frame_index = 0

    def animate_boss_explosion(self):
        if self.boss_explosion_animation_running:
            if self.boss_explosion_frame_index == 0:
                self.boss_explosion_animation = self.boss_explosion_animations[0]
            self.boss_explosion_frame_index += self.animation_speed
            
            if self.boss_explosion_frame_index >= len(self.boss_explosion_animation):
                self.boss_explosion_animation_running = False
                return

            self.boss_explosion_image = self.boss_explosion_animation[int(self.boss_explosion_frame_index)]
            self.boss_explosion_image = scale(self.boss_explosion_image, 'mult', coeff/2)
        
    def draw_boss_explosion(self,screen):
        if self.boss_explosion_animation_running:
            screen.blit(self.boss_explosion_image, (self.rect.centerx-self.boss_explosion_image.get_width()/2 , self.rect.centery-self.boss_explosion_image.get_height()/2))

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
                self.attack_boost = 1
                self.effect_timer = 0
                self.effect_ongoing = False
                self.resistance = 1
                self.attack_speed_boost = 1

    def fighting(self):
        if self.flip:
            self.attack_rect.x = self.rect.centerx - self.attack_rect.width
            self.attack_rect.y = self.rect.top
        else:
            self.attack_rect.x = self.rect.centerx
            self.attack_rect.y = self.rect.top
        
        self.animation_state = 'Attack'
        self.special_animation = True
        self.frame_index = 0
   
    def damage(self, opponent_attack, opponent_attack_boost, opponent_flip):
        self.regeneration_timer = 0
        self.health -= opponent_attack*opponent_attack_boost/self.resistance
        if opponent_attack > 30:
            self.push = 20*opponent_attack/2/self.player_hitbox[0]
        else :
            self.push = 20*opponent_attack/1.2/self.player_hitbox[0]
        self.opponent_flip = opponent_flip
        self.animation_state = 'Hit'
        self.check_hit_freeze = random.choice([False, False, True])
        self.special_animation = True
        self.frame_index = 0  
        if self.health < 0:
            self.health = 0

    def update_regeneration(self):
        if self.regeneration_timer < 75:
            self.regeneration_timer += 0.1
        else:
            self.regenerate()

        
    def regenerate(self):
        if self.health < self.max_health and not self.dead:
            self.health += 0.1

    def check_freeze(self):
        if self.special_animation and not self.dead:
            if self.animation_state != 'Hit':
                self.freeze()
                if self.check_invincible:
                    self.invincible()
                else:
                    self.not_invincible()
            elif not self.check_hit_freeze:
                self.freeze()

        elif not self.special_animation or self.dead:
            self.unfreeze()
            self.not_invincible()

    def push_update(self):          
        self.push -= 1
        if self.push < 0:
            self.push = 0
        if self.opponent_flip:
            self.rect.x -= self.push/self.resistance
        else:
            self.rect.x += self.push/self.resistance
    
    def void(self):
        if self.rect.top > max_map_height:
            self.health = 0

    def death(self):
        if self.health <= 0:
            self.special_animation = True
            self.freeze()
            self.animation_state = 'Death'
            self.dead = True
            self.stamina = 0

    def draw_player(self, screen):
        mask = pygame.mask.from_surface(self.image)

        if self.flip:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff) - self.flip_offset, self.rect.y-(self.player_offset[1]*coeff)))
            if self.effect_ongoing: screen.blit(mask.to_surface(unsetcolor=(255,255,255,0), setcolor=(self.effect_color)), (self.rect.x-(self.player_offset[0]*coeff) - self.flip_offset, self.rect.y-(self.player_offset[1]*coeff)))
        else:
            screen.blit(self.image, (self.rect.x-(self.player_offset[0]*coeff), self.rect.y-(self.player_offset[1]*coeff)))
            if self.effect_ongoing: screen.blit(mask.to_surface(unsetcolor=(255,255,255,0), setcolor=(self.effect_color)), (self.rect.x-(self.player_offset[0]*coeff), self.rect.y-(self.player_offset[1]*coeff)))

    def update(self,screen):
        self.shoot_timer_update()
        self.check_shoot_input()
        if not self.freezed and not self.dead: self.get_input()
        else: self.attack_rect_update()
        self.check_attack_input()
        self.speed_fix()
        self.sprint()
        self.wall_slide()
        self.check_down_movement()
        self.update_regeneration()
        self.push_update()
        self.check_freeze()
        self.void()
        self.death()

        if not self.death_animation_stop:
            self.get_animation_state()
            self.animate()
            self.check_animation_change()
            self.update_dust_animation(screen)
            self.update_dust_animation_allow()
            self.animate_boss_explosion()

        self.draw_player(screen)
        self.draw_cursor(screen)

        if self.shell:
            self.shell.update(screen)
        if self.grenade:
            self.grenade.update(screen)

        self.grenade_countdown()

        # saves
        self.animation_state_save, self.dust_animation_state_save = self.animation_state, self.dust_animation_state
        self.direction_save = deepcopy(self.direction)
        self.shoot_allowed_save = self.shoot_allowed
        self.draw_boss_explosion(screen)