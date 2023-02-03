import pygame
from settings import coeff, tile_size
from functions import scale, get_mask


class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.image = pygame.image.load('DWARF/Tiles/'+path).convert_alpha()
        self.image = scale(self.image,'mult',coeff)
        self.rect = self.image.get_rect()
        self.rect.x = x*tile_size*coeff - tile_size*coeff
        self.rect.y = y*tile_size*coeff - tile_size*coeff

    
    def update(self, x_shift):
        self.rect.x += x_shift


class Tile_special(pygame.sprite.Sprite):
    def __init__(self,x,y,path,list,index,choice):
        super().__init__()
        if choice == 1:
            self.image = pygame.image.load('DWARF/Tiles/'+path).convert_alpha()
            self.image = scale(self.image,'mult',coeff)
            self.rect = self.image.get_rect(topleft = ((x*tile_size*coeff - tile_size*coeff  ,  y*tile_size*coeff -tile_size*coeff+2*coeff)))
        else:
            self.image = pygame.image.load('DWARF/Tiles/'+path+str(list[index])+'.png').convert_alpha()
            self.image = scale(self.image,'mult',coeff)
            self.rect = self.image.get_rect(topleft = ((x*tile_size*coeff - tile_size*coeff  ,  y*tile_size*coeff -tile_size*coeff+2*coeff)))
    
    def update(self, x_shift):
        self.rect.x += x_shift