import numpy as np
import pygame
from moviepy.editor import VideoFileClip
import math as math
from Setting import *

fonts = pygame.font.Font("ThaleahFat.ttf", 75)


# Classes

class Menu:
    def __init__(self):

        self.menu = 0
        self.video = Video("Bosque - 111101.mp4", screen_width, screen_height)
        self.bar = LoadingBar()

        self.confirm = -1

        self.y_coord = 205
        self.Start = Buttons("START", 290, 200, 400, 100, True, 75, 12,
                             (57, 193, 178))  # Message, x,y,width,hight,bool,size_of_font,radius border,color)
        self.Quit = Buttons("QUIT", 290, 400, 400, 100, True, 75, 12, (36, 148, 50))

        # Title and sprites
        self.y = 80
        self.sin_increment = 0
        self.title = Sprites(340, self.y, "dwarf.png", 1)
        # music variables
        self.volume = 1
        self.background_music = window("Dwarf", "night-city-knight-127028.mp3", self.volume)
        self.play_music = True
        self.music_on = Sprites(5, 5, "mute_on.png", 1)
        self.music_off = Sprites(5, 5, "mute_off.png", 1)
        self.mute = False
        self.background_music.play()

        # import class for creation of characters page
        self.char_page = page_characters()

    def create_menu(self, screen, game_start_variable):

        if self.play_music:
            self.background_music.play()
            self.play_music = False
        if self.menu == 0:

            # PLays the video one time
            self.video.Play(screen)
            self.y += (math.sin(self.sin_increment) * 1)
            self.sin_increment += 0.1
            self.title = Sprites(380, self.y, "dwarf.png", 1)
            self.title.detect_click(screen)

            game_start_variable, self.y_coord, self.confirm = cursor_menu(screen,
                                                                          190 + (math.sin(self.sin_increment) * 10),
                                                                          self.y_coord, game_start_variable)
            if self.Start.draw(screen) or self.confirm == 0:
                print("Start")
                self.menu = 1
            if self.Quit.draw(screen) or self.confirm == 1:
                print("Quit")
                game_start_variable = False

            # Mute the sound
            if not self.mute:
                if self.music_on.detect_click(screen):
                    self.mute = True
                    self.background_music.set_volume(0)
            else:
                if self.music_off.detect_click(screen):
                    self.background_music.set_volume(1)
                    self.mute = False

        elif self.menu == 1:
            self.menu = self.char_page.put(screen,self.menu)
        elif self.menu == 2:
            self.bar.create_bar(screen)
        return game_start_variable


class Buttons:
    def __init__(self, text, x, y, width, height, state, font_size, radius, color):
        self.x = x
        self.y = y
        self.savey = y + 5
        self.w = width
        self.h = height
        self.text = text
        self.f_size = font_size
        # create rectangles
        self.upper_rect = pygame.Rect((x, y), (self.w, self.h))
        self.down_rect = pygame.Rect((x + 4, y + 10), (self.w * 0.98, self.h * 0.98))
        self.colorc = (40, 40, 40)
        self.colortext = (255, 255, 255)
        self.topcolor = color
        self.save_color = color

        self.texto = pygame.font.Font("ThaleahFat.ttf", self.f_size).render(self.text, True, self.colortext)
        self.text_rect = self.texto.get_rect(center=self.upper_rect.center)
        self.rad = radius
        self.clicked = False
        self.was_pressed = False
        self.alt = state
        self.colorbool = False

    def animation(self, x, y, w, h, texte_rec, topcolor):
        color = topcolor
        rectangle = pygame.Rect((x, y), (w, h))
        texte = texte_rec.get_rect(center=rectangle.center)
        return color, rectangle, texte

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        # print(y_curseur)#205
        # print(self.savey)#200
        self.texto = pygame.font.Font("ThaleahFat.ttf", self.f_size).render(self.text, True, self.colortext)
        if self.down_rect.collidepoint(pos) or self.upper_rect.collidepoint(pos):
            if not self.clicked and self.was_pressed and not self.alt:  # hover black and white
                self.topcolor = (255, 255, 255)
                self.colortext = (0, 0, 0)
                self.upper_rect = pygame.Rect((self.x, self.y - 4), (self.w, self.h))
                self.text_rect = self.texto.get_rect(center=self.upper_rect.center)

            if self.alt:  # this variable is used to do it one time
                if pygame.mouse.get_pressed()[0] == 0:
                    self.was_pressed = True
                else:
                    self.was_pressed = False

                self.alt = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True

        else:
            if pygame.mouse.get_pressed()[0] == 0:  # return color to normal
                self.colortext = (255, 255, 255)
                self.topcolor = self.save_color
                if (not self.alt):
                    self.upper_rect = pygame.Rect((self.x, self.y), (self.w, self.h))
                    self.text_rect = self.texto.get_rect(center=self.upper_rect.center)

            self.alt = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
            self.topcolor, self.upper_rect, self.text_rect = self.animation(self.x, self.y, self.w, self.h, self.texto,
                                                                            self.save_color)
            self.alt = True

            if self.down_rect.collidepoint(pos) or self.upper_rect.collidepoint(pos):
                action = True

        if self.clicked and self.was_pressed:  # creates the animation while holding
            self.colortext = (255, 255, 255)  # return color text to normal
            self.topcolor, self.upper_rect, self.text_rect = self.animation(self.x, self.y + 10, self.w, self.h,
                                                                            self.texto,
                                                                            (45, 56, 70))

        pygame.draw.rect(screen, self.colorc, self.down_rect, border_radius=self.rad)
        pygame.draw.rect(screen, self.topcolor, self.upper_rect, border_radius=self.rad)
        screen.blit(self.texto, self.text_rect)
        return action


class Options:
    def __init__(self, image, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.pos = (x, y)


class Video:
    def __init__(self, video_file, w, h):
        self.video = VideoFileClip(video_file)
        self.video_width, self.video_height = w, h
        self.scaled_width = w
        self.scaled_height = h
        self.frame_iter = iter(self.video.iter_frames())

    def Play(self, screen):
        try:
            # Get the next frame
            frame = next(self.frame_iter)
            # Convert the frame to a Pygame surface
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (self.scaled_width, self.scaled_height))
            # Blit the frame to the screen
            screen.blit(frame, (0, 0))
            pygame.time.wait(20)
        except:
            # Reset the frame_iter if all frames have been retrieved
            self.frame_iter = iter(self.video.iter_frames())


class LoadingBar:
    def __init__(self):
        self.bar = pygame.Rect((190, 200), (400, 100))
        self.width = 75
        self.increase = 1
        self.loading_bar = pygame.Rect((210, 212), (1, 75))

    def create_bar(self, screen):
        screen.fill((0, 0, 0))
        text_creation("Loading", (pygame.font.Font("ThaleahFat.ttf", 75)), (255, 255, 255), 280, 100, screen)
        pygame.draw.rect(screen, (255, 255, 255), self.bar, 5, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), self.loading_bar, border_radius=2)
        if self.loading_bar.width < 360:
            self.increase += 0.05
            self.loading_bar.width = self.width + self.increase


class Sprites(pygame.sprite.Sprite):
    def __init__(self, x, y, image, coef):
        super().__init__()
        self.image = pygame.image.load(image)
        self.s, self.h = self.image.get_size()
        self.coef = coef
        self.scaled_width = int(self.s * self.coef)
        self.scaled_height = int(self.h * self.coef)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Create a sprite group
        self.sprites = pygame.sprite.Group()

        # Add the sprite to the group
        self.sprites.add(self)
        # self.alt = state
        self.clicked = False
        self.was_pressed = False
        self.execute = False

    def detect_click(self, screen):
        # Check if the mouse is over the sprite
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            action = True
            self.clicked = False
        self.sprites.draw(screen)
        return action


# Funtions

def text_creation(text, font, textcol, x, y, screen):
    img = font.render(text, True, textcol)
    screen.blit(img, (x, y))


def window(Title_window, Music, Volume):
    pygame.display.set_caption(Title_window)
    background_music = pygame.mixer.Sound(Music)
    background_music.set_volume(Volume)
    return background_music


def cursor_menu(screen, x, y, game_start_variable):
    image = pygame.image.load("cursort.png")
    s, h = image.get_size()
    coef = 4
    scaled_width = int(s * coef)
    scaled_height = int(h * coef)
    select = -1
    # Scale the image
    image = pygame.transform.scale(image, (scaled_width, scaled_height))
    cord_y = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_start_variable = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and y > 205:
                cord_y -= 200
            else:
                if event.key == pygame.K_DOWN and y < 405:
                    cord_y += 200
            if event.key == pygame.K_SPACE and (y == 205):
                select = 0
            elif event.key == pygame.K_SPACE and (y == 405):
                select = 1
    y += cord_y
    screen.blit(image, (x, y))
    return game_start_variable, y, select


class page_characters:
    def __init__(self):
        self.x = 150
        self.hero = Sprites(self.x, 200, "Hero.png", 8)
        self.halo = Sprites(self.x + 250, 180, "Halo.png", 7)
        self.gladiator = Sprites(self.x + 500, 180, "Gladiator.png", 6.5)
        self.herostext_font = pygame.font.Font("ThaleahFat.ttf", 30)

        self.back_char = pygame.image.load("tabern.jpg")
        self.s, self.h = self.back_char.get_size()
        self.coef = 0.5
        self.scaled_width = int(self.s * self.coef)
        self.scaled_height = int(self.h * self.coef)
        self.back_char = pygame.transform.scale(self.back_char, (self.scaled_width, self.scaled_height))

        self.y = 10
        self.sin_increment = 0
        self.back = Buttons("Back",20,430,150,80,True,50,12,(83,11,20))
        self.play_game= Buttons("Play",780,430,150,80,True,50,12,(11,83,29))

    def put(self, screen,menu):
        screen.blit(self.back_char, (0, 0))
        self.y += (math.sin(self.sin_increment) * 0.05)
        self.sin_increment += 0.005
        text_creation("Select you Hero", fonts, (255, 255, 255), 200, self.y, screen)
        text_creation("HERO", self.herostext_font, (255, 255, 255), self.x+50, 370, screen)
        text_creation("HALO", self.herostext_font, (255, 255, 255), self.x + 290, 370, screen)
        text_creation("GLADIATOR", self.herostext_font, (255, 255, 255), self.x + 500, 370, screen)
        self.play_game.draw(screen)

        if self.back.draw(screen):
            menu = 0
        if self.hero.detect_click(screen):
            print("Hero")
        if self.halo.detect_click(screen):
            print("Halo")
        if self.gladiator.detect_click(screen):
            print("gladiator")
        return menu
