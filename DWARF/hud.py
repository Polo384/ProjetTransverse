import pygame
from settings import screen_width, coeff
from functions import scale, greyscale
from math import floor

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

    def update(self,screen):
        self.update_health_bar_color()
        self.update_death()
        self.update_process_bar()

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

    #health bar above heroes
        if not self.player.dead:
            self.hero_barbg.centerx = self.player.rect.centerx
            self.hero_barbg.y = self.player.rect.y - 25
            self.hero_bar.centerx = self.player.rect.centerx
            self.hero_bar.y = self.player.rect.y - 25

            #on the left
            self.hero_bar.x = self.hero_barbg.x
            self.hero_bar.width = coeff*25*self.player.health/self.player.max_health

            self.process_hero_bar.width = self.process_hero_bar_width
            self.process_hero_bar.centerx = self.player.rect.centerx
            self.process_hero_bar.y = self.player.rect.y - 25
            self.process_hero_bar.x = self.hero_barbg.x
            
            pygame.draw.rect(screen, (186,186,186), self.hero_barbg)
            pygame.draw.rect(screen, "white", self.process_hero_bar)
            pygame.draw.rect(screen, self.health_bar_color, self.hero_bar)
        

