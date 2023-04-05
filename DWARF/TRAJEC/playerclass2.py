import pygame
from projectilesclass2 import *
import math
import sys


class Player():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = 5
        self.shoot = False
        self.input_keys = {'jump': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'sprint': pygame.K_LSHIFT, 'shoot': pygame.K_f, 'power': pygame.K_r}
        self.freezed = False
        self.angle = 0
        self.time_pressed = 0
        self.shoot = False
        self.ball = None
        self.time = 0

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, 100, 100))
        self.rectx = self.rect.centerx
        self.recty = self.rect.centery

    def freezed_on(self):
        self.freezed = True

    def freezed_off(self):
        self.freezed = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.input_keys['right']] and keys[self.input_keys['left']]:
            self.x = self.x
        elif keys[self.input_keys['right']]:
            self.x += self.velocity
        elif keys[self.input_keys['left']]:
            self.x -= self.velocity
        elif keys[self.input_keys['shoot']] and not self.freezed:
            self.freezed_on()
        elif keys[self.input_keys['shoot']] and self.freezed:
            self.freezed_off()

    def get_input2(self):
        keys = pygame.key.get_pressed()

        if keys[self.input_keys['shoot']]:
            self.freezed_off()
        elif keys[self.input_keys['jump']]:
            self.angle -= 5
        elif keys[self.input_keys['down']]:
            self.angle += 5
        elif keys[self.input_keys['power']]:
            self.shoot = True

    def cursor(self, screen):
        distance = 150
        cursorx = int(self.rectx + distance * math.cos(math.radians(self.angle)))
        cursory = int(self.recty + distance * math.sin(math.radians(self.angle)))
        pygame.draw.circle(screen, (255, 255, 255), (cursorx, cursory), 5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame
