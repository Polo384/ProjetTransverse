import pygame
from settings import coeff
from functions import scale

class BG(pygame.sprite.Sprite):
    def __init__(self, choice, number):
        super().__init__()
        self.number = number
        if choice == 1 or choice == 2:
            bg_image = pygame.image.load(f'DWARF/Backgrounds/Sky{choice}/{number}.png').convert_alpha()
        else:
            bg_image = pygame.image.load(f'DWARF/Backgrounds/Menu_BG/{number}.png').convert_alpha()
        bg_image = scale(bg_image, 'mult', coeff)

        self.image = pygame.Surface((bg_image.get_width()*2, bg_image.get_height()), flags=pygame.SRCALPHA)
        self.image.blit(bg_image, (0, 0))
        self.image.blit(bg_image, (bg_image.get_width(), 0))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.Vector2(self.rect.topleft)
        
    def update(self):
        self.pos.x -= 0.075*coeff*self.number
        self.rect.x = int(self.pos.x)
        if self.rect.centerx <= 0:
            self.pos.x = 0