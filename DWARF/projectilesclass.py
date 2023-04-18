import pygame
import math
from functions import scale
from settings import coeff

class Projectiles2():
    def __init__(self,x,y, angle, choice, flip):
        self.image = pygame.image.load(f'DWARF/Projectiles/shell_p{choice}.png').convert_alpha()
        self.image = scale(self.image, 'mult', 2.5/3*coeff)
        if flip: self.flip_image()

        self.rect = pygame.Rect(x, y, self.image.get_width() , self.image.get_height())
        self.start_x, self.start_y = x, y
        self.rect.x, self.rect.y = x, y

        self.power = 50
        self.angle = angle
        self.time = 1
        self.time_incrementation = 0.5
        self.rotation_factor = 0
        self.rotation_factor_value = 20
        self.distX, self.distX_save, self.distY, self.distY_save = 0, 0, 0, 0
        self.x_collision_factor = 1

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def rotation(self):
        self.rotation_factor += self.rotation_factor_value
        self.rotation_factor %= 360
        self.image_copy = pygame.transform.rotate(self.image, self.rotation_factor)
        
    def update(self, screen):
        #self.rotation()
        self.time += self.time_incrementation

        self.distX_save = self.distX
        self.distY_save = self.distY

        self.distX = math.cos(math.radians(self.angle)) * self.power * self.time * self.x_collision_factor
        self.distY = ((math.sin(math.radians(self.angle)) * self.power * self.time) + ((-2.75 * (self.time ** 2)) / 2) ) 

        self.rect.x = round(self.start_x + self.distX)
        self.rect.y = round(self.start_y - self.distY)

        screen.blit(self.image, (self.rect.centerx, self.rect.centery))
        #screen.blit(self.image_copy, (self.rect.centerx - int(self.image_copy.get_width()/2), self.rect.centery - int(self.image_copy.get_height()/2)))


        
class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y 
        self.radius = 5
        self.color = ((255,0,0))
        self.power = 10

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius-1)
    
    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        #we calculate the trajectory of the ball 
        angle = ang
        velx = math.cos(angle) * power #here we calculate the vx
        vely = math.sin(angle) * power #here we calaculate vy

        #here we have the equation of x and y (physic course: in french it's équation horaires)
        distX = velx * time
        distY = (vely * time) + ((-9.81 * (time ** 2)) / 2)

        #we calculate the new coordonates of x and y 
        newx = round(distX + startx)
        newy = round(starty - distY)


        return (newx, newy)
