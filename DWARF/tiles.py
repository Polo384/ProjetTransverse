import pygame
from settings import coeff, tile_size
from functions import scale


class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.image = pygame.image.load('DWARF/Tiles/'+path).convert_alpha()
        self.image = scale(self.image,'mult',coeff)
        self.rect = self.image.get_rect()
        self.rect.x = x*tile_size*coeff - tile_size*coeff - 3*coeff
        self.rect.y = y*tile_size*coeff - 2*tile_size*coeff + 3*coeff

class Tile_Specific(pygame.sprite.Sprite):
    def __init__(self,x,y,path, up,down,left,right):
        super().__init__()
        
        if up: up_size = 4*coeff
        else: up_size = 0
        if down: down_size = 4*coeff
        else: down_size = 0
        if left: left_size = 4*coeff
        else: left_size = 0
        if right: right_size = 4*coeff
        else: right_size = 0

        self.image = pygame.image.load('DWARF/Tiles/'+path).convert_alpha()
        self.image = scale(self.image,'mult',coeff)
        self.rect = pygame.Rect(0+left_size,0+up_size,tile_size*coeff - left_size - right_size,tile_size*coeff - up_size - down_size)
        self.rect.x = x*tile_size*coeff - tile_size*coeff - 3*coeff
        self.rect.y = y*tile_size*coeff - 2*tile_size*coeff + 3*coeff

class Tile_special(pygame.sprite.Sprite):
    def __init__(self,x,y,path,list,index,choice):
        super().__init__()
        if choice == 1:
            self.image = pygame.image.load('DWARF/Tiles/'+path).convert_alpha()
            self.image = scale(self.image,'mult',coeff)
            self.rect = self.image.get_rect(topleft = ((x*tile_size*coeff - tile_size*coeff - 3*coeff ,  y*tile_size*coeff - 2*tile_size*coeff + 2*coeff + 3*coeff)))
        else:
            self.image = pygame.image.load('DWARF/Tiles/'+path+str(list[index])+'.png').convert_alpha()
            self.image = scale(self.image,'mult',coeff)
            self.rect = self.image.get_rect(topleft = ((x*tile_size*coeff - tile_size*coeff - 3*coeff ,  y*tile_size*coeff - 2*tile_size*coeff + 2*coeff + 3*coeff)))
    
    def update(self, x_shift):
        self.rect.x += x_shift