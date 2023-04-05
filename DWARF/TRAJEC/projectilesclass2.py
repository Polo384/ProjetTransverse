import pygame
import math

class Projectiles():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y 
        self.radius = radius
        self.color = color

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
