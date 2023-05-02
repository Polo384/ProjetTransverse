import pygame
from settings import screen_width, screen_height, coeff
from functions import scale, greyscale
from math import floor, sin, pi

class HUD:
    def __init__(self, player, hero, choice):
        self.choice = choice
        self.player = player
        self.check_greyscale = False

        # icon hero
        self.photo = pygame.image.load(f'DWARF/Hud/{hero}_photo.png').convert_alpha()
        self.photo = scale(self.photo, 'mult', coeff*5/3)

        # health bar
        self.health_bar = pygame.image.load('DWARF/Hud/health_bar.png').convert_alpha()
        self.health_bar = scale(self.health_bar, 'mult', coeff*5/3)
        self.health_bar_color = (206,76,76)
        if self.choice ==1:
            self.process_bar_width = coeff*68.5*self.player.health/self.player.max_health
        else:
            self.process_bar_width = coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health)

        # shadow on health bar
        self.font = pygame.font.Font('DWARF/Hud/pixel_font.ttf', int(coeff/3*26))
        self.shadow_health = pygame.Surface((coeff*68.5, coeff*7.5/3), pygame.SRCALPHA)
        self.shadow_health.fill((0,0,0))
        self.shadow_health.set_alpha(50)

        # stamina bar
        self.stamina_image = pygame.image.load('DWARF/Hud/stamina_bar.png')
        self.stamina_image = scale(self.stamina_image, 'mult', coeff*5/3)
        self.stamina_image_color = (75,175,194)

        # shadow on stamina bar
        self.shadow_stamina = pygame.Surface((coeff*55, coeff*6/3), pygame.SRCALPHA)
        self.shadow_stamina.fill((0,0,0))
        self.shadow_stamina.set_alpha(50)
        
        # bonus
        self.bonus_frame = scale(pygame.image.load('DWARF/Hud/bonus_frame.png').convert_alpha(), 'mult', coeff*4/3)

        #hero bar
        self.hero_barbg = pygame.Rect( 1, self.player.rect.y - 25 , coeff*25 , 2*coeff*5/3)
        self.hero_bar = pygame.Rect( 1, self.player.rect.y - 25 , coeff*25*self.player.health/self.player.max_health , 2*coeff*5/3)
        self.process_hero_bar_width = coeff*25*self.player.health/self.player.max_health
        self.process_hero_bar = pygame.Rect(1, self.player.rect.y - 25, self.process_hero_bar_width, 2*coeff*5/3)
        self.above_health_bar_timer = 50

        self.above_sprint_bar = pygame.Rect( 1, self.player.rect.y - 20 , coeff*25*self.player.stamina/self.player.max_stamina , coeff*5/3)
        self.above_sprint_bar_timer = 12


        #transformation for the right part (second hero) of the screen
        if self.choice == 2:
            self.photo = pygame.transform.flip(self.photo, True, False)
            self.health_bar = pygame.transform.flip(self.health_bar, True, False)
            self.stamina_image = pygame.transform.flip(self.stamina_image, True, False)       
        

    def update_health_bar_color(self):
        if self.player.health/self.player.max_health > 0.6:
            self.health_bar_color  = (206,76,76)
        elif self.player.health/self.player.max_health <= 0.6  and  self.player.health/self.player.max_health > 0.25:
            self.health_bar_color = (175,48,53)
        else:
            self.health_bar_color = (137,12,31)

    def update_death(self):
        if self.player.dead and not self.check_greyscale:
            self.photo = greyscale(self.photo)
            self.health_bar = greyscale(self.health_bar)
            self.check_greyscale = True
            self.stamina_image = greyscale(self.stamina_image)
            self.bonus_frame = greyscale(self.bonus_frame)

    def update_process_bar(self):
        if self.choice == 1:
            if self.process_bar_width > coeff*68.5*self.player.health/self.player.max_health:
                self.process_bar_width -= 1
            elif self.process_bar_width < coeff*68.5*self.player.health/self.player.max_health:
                self.process_bar_width = coeff*68.5*self.player.health/self.player.max_health
            
        else:
            if self.process_bar_width > coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health):
                self.process_bar_width -= 1
            elif self.process_bar_width < coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health):
                self.process_bar_width = coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health)

        if self.process_hero_bar_width > coeff*25*self.player.health/self.player.max_health:
            self.process_hero_bar_width -= 0.25

        elif self.process_hero_bar_width < coeff*25*self.player.health/self.player.max_health:
            self.process_hero_bar_width = coeff*25*self.player.health/self.player.max_health
            

    def detect_bonus(self, screen):
        if self.player.effect_ongoing :
            if self.player.speed_boost != 1:
                self.current_bonus = 'speed'
            elif self.player.attack_boost != 1:
                self.current_bonus = 'attack'
            elif self.player.resistance != 1:
                self.current_bonus = 'resistance'
            elif self.player.attack_speed_boost != 1:
                self.current_bonus = 'attack_speed'
            else:
                self.current_bonus = 'health'
            
            self.display_current_bonus(screen)

    def display_current_bonus(self, screen):
        bonus_image = scale(pygame.image.load(f'DWARF/Bonus/bonus_{self.current_bonus}.png').convert_alpha(), 'mult', coeff*4/3)

        if self.choice == 1:
            screen.blit(bonus_image, (coeff*4/3*129, coeff*4/3*7))
        else:
            screen.blit(bonus_image, (screen_width - bonus_image.get_width() - coeff*4/3*129, coeff*4/3*7))

    def above_health_bar_timer_update(self, screen):
        if self.player.animation_state == 'Hit':
            self.above_health_bar_timer = 0
            self.display_above_health_bar(screen)

        elif self.above_health_bar_timer < 50:
            self.above_health_bar_timer += 0.1
            self.display_above_health_bar(screen)

    def display_above_health_bar(self, screen):
        if not self.player.dead:
            self.hero_barbg.centerx = self.player.rect.centerx
            self.hero_barbg.y = self.player.rect.y - coeff*11
            self.hero_bar.y = self.player.rect.y - coeff*11

            #on the left
            self.hero_bar.x = self.hero_barbg.x
            self.hero_bar.width = coeff*25*self.player.health/self.player.max_health

            self.process_hero_bar.width = self.process_hero_bar_width
            self.process_hero_bar.centerx = self.player.rect.centerx
            self.process_hero_bar.y = self.player.rect.y - coeff*11
            self.process_hero_bar.x = self.hero_barbg.x
            
            # contour gris  :  pygame.draw.rect(screen, (47,47,46), pygame.Rect(self.hero_barbg.left - coeff, self.hero_barbg.top - coeff, self.hero_barbg.width + 2*coeff, self.hero_barbg.height + 2*coeff))
            pygame.draw.rect(screen, (186,186,186), self.hero_barbg, 30)
            pygame.draw.rect(screen, "white", self.process_hero_bar)
            pygame.draw.rect(screen, self.health_bar_color, self.hero_bar)

    def above_sprint_bar_timer_update(self, screen):
        if self.player.sprinting:
            self.above_sprint_bar_timer = 0
            self.display_above_sprint_bar(screen)

        elif self.above_sprint_bar_timer < 30:
            self.above_sprint_bar_timer += 0.1
            self.display_above_sprint_bar(screen)
    
    def display_above_sprint_bar(self, screen):
        if not self.player.dead:
            self.hero_barbg.centerx = self.player.rect.centerx
            self.above_sprint_bar.centerx = self.player.rect.centerx
            self.above_sprint_bar.y = self.player.rect.y - coeff*7

            #on the left
            self.above_sprint_bar.x = self.hero_barbg.x
            self.above_sprint_bar.width = coeff*25*self.player.stamina/self.player.max_stamina
            pygame.draw.rect(screen, 'white', self.above_sprint_bar)

    def charge_projectile(self):
        self.charge = pygame.Surface((coeff*19,coeff*19*(1-self.player.shoot_timer/self.player.max_shoot_timer)), pygame.SRCALPHA)
        self.charge.fill((200, 200, 200))
        self.charge.set_alpha(100)
        self.charge_rect = self.charge.get_rect()
        if self.choice == 1:
            self.charge_rect.left = 645
            self.charge_rect.bottom = 85
        else:
            self.charge_rect.left = screen_width-695
            self.charge_rect.bottom = 85

    def update(self,screen):
        self.update_health_bar_color()
        self.update_death()
        self.update_process_bar()
        self.above_health_bar_timer_update(screen)
        self.above_sprint_bar_timer_update(screen)

        if self.choice == 1:
            # photo
            screen.blit(self.photo, (coeff*3, coeff*3))

            # health
            screen.blit(self.health_bar, (coeff*63, coeff*10))
            pygame.draw.rect(screen, (230,230,230), pygame.Rect(coeff*83, coeff*15, self.process_bar_width , 5*coeff*5/3))
            pygame.draw.rect(screen, self.health_bar_color, pygame.Rect(coeff*83, coeff*15, coeff*68.5*self.player.health/self.player.max_health , 5*coeff*5/3))
            screen.blit(self.shadow_health, (coeff*83, coeff*21.5))
            screen.blit(self.font.render(str((int(self.player.health))), False, 'white'), (coeff*112, coeff*16))

            #stamina
            screen.blit(self.stamina_image, (coeff*63, coeff*32))
            pygame.draw.rect(screen, self.stamina_image_color, pygame.Rect(coeff*81, coeff*37, coeff*55.8*self.player.stamina/self.player.max_stamina, 3*coeff*5/3))
            screen.blit(self.shadow_stamina, (coeff*81, coeff*40))

            # bonus
            screen.blit(self.bonus_frame, (coeff*4/3*124, coeff*4/3*2))
            self.detect_bonus(screen)
            if self.player.effect_ongoing:
                screen.blit(self.font.render(str(int((self.player.effect_duration-self.player.effect_timer)*10/60)+1), False, 'white'), (coeff*200, coeff*16))

            #projectile
            if self.player.current_weapon:
                screen.blit(scale(pygame.image.load("DWARF/Hud/shell_frame_below.png"), 'mult', 3), (635, 22))
            else:
                screen.blit(scale(pygame.image.load("DWARF/Hud/grenade_frame_below.png"), 'mult', 3), (635, 22))
            if self.player.shoot_timer_incrementation:
                self.charge_projectile()
                screen.blit(self.charge, self.charge_rect)
                screen.blit(scale(pygame.image.load("DWARF/Hud/projectile_frame.png"), 'mult', 3), (635, 22))

        else:
            # photo
            screen.blit(self.photo, (screen_width - self.photo.get_width() - coeff*3, coeff*3))

            # health
            screen.blit(self.health_bar, (screen_width - self.health_bar.get_width() - coeff*63, coeff*10))
            pygame.draw.rect(screen, (230,230,230), pygame.Rect(screen_width - self.process_bar_width, coeff*15, coeff*68.5*self.player.health/self.player.max_health, 5*coeff*5/3))
            pygame.draw.rect(screen, self.health_bar_color, pygame.Rect(screen_width - (coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health)), coeff*15, coeff*68.5*self.player.health/self.player.max_health, 5*coeff*5/3))
            screen.blit(self.shadow_health, (screen_width - coeff*151.3, coeff*21.5))
            screen.blit(self.font.render(str((int(self.player.health))), False, 'white'), (screen_width - coeff*120, coeff*16))

            #stamina
            screen.blit(self.stamina_image, (screen_width - self.stamina_image.get_width() - coeff*63, coeff*32))
            pygame.draw.rect(screen, self.stamina_image_color, pygame.Rect(screen_width -(coeff*136 - coeff*55*(1-self.player.stamina/self.player.max_stamina)) , coeff*37, coeff*55*self.player.stamina/self.player.max_stamina, coeff*5))
            screen.blit(self.shadow_stamina, (screen_width - coeff*136.3, coeff*40))

            #bonus
            screen.blit(self.bonus_frame, (screen_width - self.bonus_frame.get_width() - coeff*4/3*124, coeff*4/3*2))
            self.detect_bonus(screen)
            if self.player.effect_ongoing:
                screen.blit(self.font.render(str(int((self.player.effect_duration-self.player.effect_timer)*10/60)+1), False, 'white'), (screen_width -coeff*207, coeff*16))
            
            #projectile
            if self.player.current_weapon:
                screen.blit(scale(pygame.image.load("DWARF/Hud/shell_frame_below.png"), 'mult', 3), (screen_width-710, 22))
            else:
                screen.blit(scale(pygame.image.load("DWARF/Hud/grenade_frame_below.png"), 'mult', 3), (screen_width-710, 22))
            if self.player.shoot_timer_incrementation:
                self.charge_projectile()
                screen.blit(self.charge, self.charge_rect)
                screen.blit(scale(pygame.image.load("DWARF/Hud/projectile_frame.png"), 'mult', 3), (screen_width-710, 22))
        
        
class WIN():
    def __init__(self, players_list):
        self.player1 = players_list[0]
        self.player2 = players_list[1]
        self.check_dead = True
        self.variable = 0
        self.levitation_factor = 0
        self.flicker_factor = 0
        self.flickered = True
        self.space_bar_image_1 = pygame.image.load('DWARF/Menu/press_space_bar_1.png').convert_alpha()
        self.space_bar_image_1 = scale(self.space_bar_image_1, 'mult', coeff*1.5)
        self.space_bar_image_2 = pygame.image.load('DWARF/Menu/press_space_bar_2.png').convert_alpha()
        self.space_bar_image_2 = scale(self.space_bar_image_2, 'mult', coeff*1.5)

        self.start, self.create_level = True, False

    def levitate(self):
        self.levitation_factor = round(sin(self.variable)*coeff*4.5)
        self.variable += 0.08

    def flicker(self):
        self.flicker_factor += 1
        if self.flicker_factor == 12:
            self.flickered = not self.flickered
            self.flicker_factor = 0

    def launch_again(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.start = False 
            
        elif keys[pygame.K_SPACE]:
            self.create_level = True

    def update(self, screen):
        if self.check_dead:
            if self.player1.dead:
                self.check_dead = False
                self.winner_image = pygame.image.load('DWARF/Menu/p2_wins.png').convert_alpha()
                self.winner_image = scale(self.winner_image, 'mult', coeff*6)

            elif self.player2.dead:
                self.check_dead = False
                self.winner_image = pygame.image.load('DWARF/Menu/p1_wins.png').convert_alpha()
                self.winner_image = scale(self.winner_image, 'mult', coeff*6)
        
        else:
            self.levitate()
            screen.blit(self.winner_image, (screen_width/2 - self.winner_image.get_width()/2  ,  coeff*65 + self.levitation_factor))

            self.flicker()
            if self.flickered:
                screen.blit(self.space_bar_image_1, (screen_width/2 - self.space_bar_image_1.get_width()/2  ,  coeff*300))
            else:
                screen.blit(self.space_bar_image_2, (screen_width/2 - self.space_bar_image_2.get_width()/2  ,  coeff*300))

            self.launch_again()

        
        
        

