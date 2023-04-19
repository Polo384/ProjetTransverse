import pygame
import math
from functions import scale
from settings import coeff

class Shell():
    def __init__(self,x,y, angle, choice, flip):
        self.image = pygame.image.load(f'DWARF/Projectiles/shell_p{choice}.png').convert_alpha()
        self.image = scale(self.image, 'mult', coeff)
        if flip: self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center = (x,y))
        self.start_x, self.start_y = x, y

        self.power = 34
        self.angle = angle
        self.rotation_angle = self.angle
        self.time = 1
        self.time_incrementation = 0.5
        self.distX, self.distX_save, self.distY, self.distY_save = 0, 0, 0, 0
        self.wind_factor = 1

    def rotation(self):
        self.rotation_angle = math.degrees(math.atan((self.distY_save - self.distY)/(self.distX_save - self.distX)))
        self.image_copy = pygame.transform.rotate(self.image, self.rotation_angle)
    
    def reduce_x_speed(self): # simuler force de frottements
        self.wind_factor *= 1.01
        self.distX -= self.wind_factor

    def update(self, screen):
        self.time += self.time_incrementation

        self.distX_save = self.distX
        self.distY_save = self.distY

        self.distX = math.cos(math.radians(self.angle)) * self.power * self.time
        self.distY = (math.sin(math.radians(self.angle)) * self.power * self.time) + ((-1.8 * (self.time ** 2)) / 2)

        self.reduce_x_speed()
        self.rotation()

        self.rect.centerx = round(self.start_x + self.distX)
        self.rect.centery = round(self.start_y - self.distY)
        screen.blit(self.image_copy, (self.rect.centerx - int(self.image_copy.get_width()/2), self.rect.centery - int(self.image_copy.get_height()/2)))

class Grenade():
    def __init__(self,x,y, x_cursor, y_cursor, choice, flip):
        self.image = pygame.image.load(f'DWARF/Projectiles/grenade_p{choice}.png').convert_alpha()
        self.image = scale(self.image, 'mult', coeff)
        if flip:
            self.flip_image()

        self.rect = self.image.get_rect(center = (x,y))
        self.x_speed, y_speed = (x_cursor - x)/5, (y_cursor - y)/4/1.5
        self.direction= pygame.math.Vector2(self.x_speed, y_speed)
        self.gravity = coeff/4/1.5
        self.bounce_value = -12

        self.rotation_factor = 0
        self.rotation_factor_value = 15

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def rotation(self):
        if abs(self.rotation_factor_value) >= 1 and abs(self.direction.x) > 1:
            self.rotation_factor_value /= 1.01
            self.rotation_factor += self.rotation_factor_value
            self.rotation_factor %= 360
            self.image_copy = pygame.transform.rotate(self.image, self.rotation_factor)
    
    def apply_bounce(self):
        self.bounce_value /= 1.5
        self.direction.x /= 1.1
        self.direction.y = self.bounce_value
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.centery += self.direction.y

    def divide_speed(self):
        self.direction.x /= 1.01

    def update(self, screen):
        self.rotation()
        self.divide_speed()
        
        screen.blit(self.image_copy, (self.rect.centerx - int(self.image_copy.get_width()/2), self.rect.centery - int(self.image_copy.get_height()/2)))