import pygame
from settings import screen_width, coeff
from functions import scale, greyscale
from time import sleep
class HUD:
    def __init__(self, player, hero, choice):
        self.choice = choice
        self.player = player
        self.check_greyscale = False

        self.photo = pygame.image.load(f'DWARF/Hud/{hero}_photo.png').convert_alpha()
        self.photo = scale(self.photo, 'mult', coeff*5/3)

        self.health_bar = pygame.image.load('DWARF/Hud/health_bar2.png').convert_alpha()
        self.health_bar = scale(self.health_bar, 'mult', coeff*5/3)
        self.health_bar_color = (206,76,76)
        self.font = pygame.font.Font('DWARF/Hud/pixel_font.ttf', int(coeff/3*26))
        self.shadow = pygame.Surface((coeff*68.5, coeff*7.5/3), pygame.SRCALPHA)
        self.shadow.fill((0,0,0))
        self.shadow.set_alpha(50)

        if self.choice == 2:
            self.photo = pygame.transform.flip(self.photo, True, False)
            self.health_bar = pygame.transform.flip(self.health_bar, True, False)


    def update_health_bar_color(self):
        if self.player.health/self.player.max_health > 0.6:
            self.health_bar_color = (206,76,76)
        elif self.player.health/self.player.max_health <= 0.6  and  self.player.health/self.player.max_health > 0.25:
            self.health_bar_color = (175,48,53)
        else:
            self.health_bar_color = (137,12,31)

    def update_death(self):
        if self.player.dead and not self.check_greyscale:
            self.photo = greyscale(self.photo)
            self.health_bar = greyscale(self.health_bar)
            self.check_greyscale = True

    def update(self,screen):
        self.update_health_bar_color()
        self.update_death()

        if self.choice == 1:
            # photo
            screen.blit(self.photo, (coeff*3, coeff*3))

            # health
            screen.blit(self.health_bar, (coeff*63, coeff*10))
            pygame.draw.rect(screen, self.health_bar_color, pygame.Rect(coeff*83, coeff*15, coeff*68.5*self.player.health/self.player.max_health , 5*coeff*5/3))
            screen.blit(self.shadow, (coeff*83, coeff*21.5))
            screen.blit(self.font.render(str((int(self.player.health))), False, 'white'), (coeff*112, coeff*16))

        else:
            # photo
            screen.blit(self.photo, (screen_width - self.photo.get_width() - coeff*3, coeff*3))

            # health
            screen.blit(self.health_bar, (screen_width - self.health_bar.get_width() - coeff*63, coeff*10))
            pygame.draw.rect(screen, self.health_bar_color, pygame.Rect(screen_width - (coeff*151.3 - coeff*68.5*(1-self.player.health/self.player.max_health)), coeff*15, coeff*68.5*self.player.health/self.player.max_health, 5*coeff*5/3))
            screen.blit(self.shadow, (screen_width - coeff*151.3, coeff*21.5))
            screen.blit(self.font.render(str((int(self.player.health))), False, 'white'), (screen_width - coeff*120, coeff*16))
            
      