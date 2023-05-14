import pygame
import math as math
from settings import screen_width, screen_height
from functions import scale
from backgrounds import*
from Heroes_Dico import *
from functions import scale
from Animation import*
from random import*
from Heroes_Dico import santa_stats
y_cord = 300
x_cord = 160
seed(57)
separation_rows = coeff*4/3*100


hero_list = ['santa','indiana_jones','adventurer','halo','dwarf','gladiator','hobbit','question_mark']

# Classes

class Menu():
    def __init__(self,all_ani):
        
        self.title = None
        self.menu = 0

        self.confirm = -1

        self.y_coord = 150*coeff

        self.play = Buttons_2(screen_width/coeff, 110*coeff,coeff/3*2, "DWARF/Menu/play.png","DWARF/Menu/play_press.png","DWARF/Menu/play_shadow.png",True)
        self.credits = Buttons_2(screen_width/coeff, 150*coeff, coeff/3*2,"DWARF/Menu/credits.png","DWARF/Menu/credits_press.png","DWARF/Menu/credits_shadow.png",True)
        self.quit = Buttons_2(screen_width/coeff, 190*coeff, coeff/3*2,"DWARF/Menu/quit.png","DWARF/Menu/quit_press.png","DWARF/Menu/quit_shadow.png",True)

        # Title and sprites
        self.y = 35*coeff
        self.sin_increment = 0
        # music variables

        self.volume = 0.8
        self.background_music = window("DWARF", "DWARF/Musics/menu.wav", self.volume)
        self.play_music = True
        self.music_on = Sprites(15*coeff, 15*coeff,False, "DWARF/Menu/mute_on.png", 1)
        self.music_off = Sprites(15*coeff, 15*coeff,False, "DWARF/Menu/mute_off.png", 1)
        self.mute = False
        self.background_music.play()

        # import class for creation of characters page
        self.char_page = page_characters()

        self.backgrounds_group = pygame.sprite.Group()
        self.backgrounds_group.add(BG(3,1),BG(3,2),BG(3,3),BG(3,4))
        
        self.Selections = selection_of_characters(all_ani)
        self.all_ani = all_ani

        self.player1 = "none"
        self.player2 = "none"

        self.create_level = False
        self.running = False

        self.pos_player1_x = 0
        self.pos_player1_y = 0

        self.pos_player2_x = 0
        self.pos_player2_y = 0

        self.cursor_main = cursor_main_menu()

        self.credits_credits = False

        self.black = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.black.fill((0, 0, 0))
        self.black.set_alpha(200)

        # credits
        alexandre = scale(pygame.image.load('DWARF/Credits/alexandre.png').convert_alpha(), 'mult', coeff*2)
        ivan = scale(pygame.image.load('DWARF/Credits/ivan.png').convert_alpha(), 'mult', coeff*2)
        paul = scale(pygame.image.load('DWARF/Credits/paul.png').convert_alpha(), 'mult', coeff*2)
        gabriel = scale(pygame.image.load('DWARF/Credits/gabriel.png').convert_alpha(), 'mult', coeff*2)
        samuel = scale(pygame.image.load('DWARF/Credits/samuel.png').convert_alpha(), 'mult', coeff*2)
        self.creators = [paul, samuel, alexandre, ivan, gabriel]
        self.names = ['Paul', 'Samuel', 'Alexandre', 'Ivan', 'Gabriel']
        self.surnames = ['CHERUBIN', 'WEISTROFFER', 'DIDIER', 'GRANDI', 'SAUTIERE']
        self.creators_increment = [0, 36, 72, 108, 144, 180]
        self.y_fix = [35,35,80,30,-25]

        # press space bar to play
        self.variable = 0
        self.flicker_factor = 0
        self.flickered = True
        self.space_bar_image_1 = pygame.image.load('DWARF/Menu/press_space_bar_1.png').convert_alpha()
        self.space_bar_image_1 = scale(self.space_bar_image_1, 'mult', coeff*1.5)
        self.space_bar_image_2 = pygame.image.load('DWARF/Menu/press_space_bar_2.png').convert_alpha()
        self.space_bar_image_2 = scale(self.space_bar_image_2, 'mult', coeff*1.5)

    def levitate(self):
        self.levitation_factor = round(math.sin(self.variable)*coeff*4.5)
        self.variable += 0.08

    def flicker(self):
        self.flicker_factor += 1
        if self.flicker_factor == 12:
            self.flickered = not self.flickered
            self.flicker_factor = 0

    def create_menu(self, screen, game_start_variable):

        if self.menu == 0:
            

            keys = pygame.key.get_pressed()
            self.create_level = False
            # PLays the video one time
            self.backgrounds_group.update()
            self.backgrounds_group.draw(screen)
            
            self.y += (math.sin(self.sin_increment) * 1)
            self.sin_increment += 0.1
            self.title = Sprites(screen_width/coeff, self.y,True, "DWARF/Menu/dwarf.png", coeff*1.25)
            if not self.credits_credits: self.title.detect_click(screen)
            if not self.credits_credits:
                game_start_variable, self.y_coord, self.confirm, self.button_choice = \
                self.cursor_main.cursor_menu(screen,135*coeff + (math.sin(self.sin_increment) * 10) ,self.y_coord, game_start_variable)
                if self.play.Update(screen, self.button_choice, 0) or self.confirm == 0:
                    self.menu = 1
                if self.credits.Update(screen, self.button_choice, 1) or self.confirm == 1:
                    self.credits_credits = True    
                if self.quit.Update(screen, self.button_choice, 2) or self.confirm == 2:
                    game_start_variable = False

            else:
                screen.blit(self.black, (0,0))
                i = 0
                for creator in self.creators:
                    y = math.sin(self.creators_increment[i])*12
                    self.creators_increment[i] += 0.1
                    screen.blit(pygame.font.Font("DWARF/Credits/Minecraft.ttf", 35).render(self.names[i], False, 'white'), (275+300*i, 225+y+self.y_fix[i]))
                    screen.blit(pygame.font.Font("DWARF/Credits/Minecraft.ttf", 38).render(self.surnames[i], False, 'white'), (275+300*i, 270+y+self.y_fix[i]))
                    screen.blit(creator, (275+300*i, 320))
                    i+=1


            if(keys[pygame.K_ESCAPE]):
                self.credits_credits =  False
            if not self.mute:
                if self.music_on.detect_click(screen):
                    self.mute = True
                    self.background_music.set_volume(0)
            else:
                if self.music_off.detect_click(screen):
                    self.background_music.set_volume(self.volume)
                    self.mute = False
                      
                    
            self.Selections = selection_of_characters(self.all_ani)
            

        elif self.menu == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.menu = 0
            self.menu = self.char_page.put(screen,self.menu)
            self.player1 , self.player2,self.pos_player1_x, self.pos_player1_y, self.pos_player2_x, self.pos_player2_y = self.Selections.create_selection(screen)
            show_data(screen,25,250,self.pos_player1_x, self.pos_player1_y,1)
            show_data(screen,1538,250,self.pos_player2_x, self.pos_player2_y,2)
            if not(self.player1 == "none" or self.player2 == "none"):
                self.flicker()
                if self.flickered:
                    screen.blit(self.space_bar_image_1, (screen_width/2 - self.space_bar_image_1.get_width()/2  ,  coeff*320))
                else:
                    screen.blit(self.space_bar_image_2, (screen_width/2 - self.space_bar_image_2.get_width()/2  ,  coeff*320))

            if(self.menu == 2 and (self.player1 == "none" or self.player2 == "none")):
                self.menu = 1
        elif self.menu == 2:
            pygame.mixer.Sound(f'DWARF/Sounds/pop.wav').play()
            self.create_level = True
            self.background_music.stop()
        
        return game_start_variable, self.player1,self.player2, self.create_level


class Buttons:
    def __init__(self, text, x, y, width, height, state, font_size, radius, color):
        self.x = x*coeff/2
        self.y = y*coeff/2
        self.savey = y + 5
        self.w = width*coeff/2
        self.h = height*coeff/2
        self.text = text
        self.f_size = int(font_size*coeff/2)
        # create rectangles
        self.upper_rect = pygame.Rect((self.x, y*coeff/2), (self.w, self.h))
        self.down_rect = pygame.Rect((self.x + 4*coeff/2, self.y + 10*coeff/2), (self.w * 0.98, self.h * 0.98))
        self.colorc = (40, 40, 40)
        self.colortext = (255, 255, 255)
        self.topcolor = color
        self.save_color = color

        self.texto = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", self.f_size).render(self.text, True, self.colortext)
        self.text_rect = self.texto.get_rect(center=self.upper_rect.center)
        self.rad = int(radius*coeff/2)
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
        self.texto = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", self.f_size).render(self.text, True, self.colortext)
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


class credits:
    def __init__(self, image, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.pos = (x, y)


class Sprites(pygame.sprite.Sprite):
    def __init__(self, x, y,take_center, image, multiplier):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = scale(self.image, 'mult', coeff*multiplier)

        self.rect = self.image.get_rect()
                

        self.rect.x = x*coeff/2
        self.rect.y = y*coeff/2
        if take_center:
            self.rect.x -= self.rect.width/2
            self.rect.y -= self.rect.height/2
            
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

def text_creation(text, font, textcol, x, y,take_center, screen):
    img = font.render(text, True, textcol)
    x = x *coeff/3
    y = y*coeff/3
    if take_center:
        rect = img.get_rect()
        x -= rect.width/2
        y -= rect.height/2
    screen.blit(img, (x, y))


def window(Title_window, Music, Volume):
    pygame.display.set_caption(Title_window)
    background_music = pygame.mixer.Sound(Music)
    background_music.set_volume(Volume)
    return background_music

class cursor_main_menu():
    def __init__(self):
        self.pressed_up = False
        self.pressed_down = False

    def cursor_menu(self,screen, x, y, game_start_variable):
        image = pygame.image.load("DWARF/Menu/cursor.png").convert_alpha()
        image = scale(image, 'mult', coeff*coeff/3*2)
        keys = pygame.key.get_pressed()
        select = -1
        
        if (keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_l]) and self.pressed_down == False:
            self.pressed_down = True
        if (keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_o]) and self.pressed_up == False:
            self.pressed_up = True 

        if self.pressed_down and not (keys[pygame.K_DOWN] or keys[pygame.K_s]or keys[pygame.K_l]):
            self.pressed_down = False
            if y <= 150*coeff:
                y = 210*coeff
            elif y == 210*coeff:
                y = 270*coeff
                
        elif self.pressed_up and not (keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_o]):
            self.pressed_up = False
            if y == 210*coeff:
                y = 150*coeff
            elif y == 270*coeff:
                y = 210*coeff

        if (y == 150*coeff):
            choice = 0
        elif (y == 210*coeff):
            choice = 1
        elif(y == 270*coeff):
            choice = 2
        
        if keys[pygame.K_SPACE]:
            select = choice

        screen.blit(image, (x, y))

        return game_start_variable, y, select, choice


class page_characters:
    def __init__(self):
        self.x = 150

        self.back_char = pygame.image.load("DWARF/Menu/white_background.png").convert_alpha()
        self.back_char = scale(self.back_char, 'mult', coeff/3)

        self.y = 45
        self.sin_increment = 0

        self.select_hero_title = pygame.image.load('DWARF/Menu/select_hero_title.png').convert_alpha()
        self.select_hero_title = scale(self.select_hero_title, 'mult', coeff*3.5)

    def put(self, screen,menu):
        screen.blit(self.back_char, (0, 0))
        self.y += round(math.sin(self.sin_increment)*1)
        self.sin_increment += 0.1
        screen.blit(self.select_hero_title, (screen_width/2 - self.select_hero_title.get_width()/2, self.y))
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_SPACE]:
            menu = 2
        if keys[pygame.K_ESCAPE]:
            menu = 0
        
        return menu


class Buttons_2():
    def __init__(self, x, y, multiplier, image, image1, shadow, state):
        self.y = y
        self.increment = 0
        #Loads images and gets their center coordenates
        self.multiplier = multiplier
        self.image, self.image1, self.shadow = load_images(image,image1,shadow,multiplier)

        self.image_rect = self.image.get_rect()
        self.image_x= x*coeff/2
        self.image_y = y*coeff/2
        
        #set the center as coordenate for positioning
        self.image_x -= self.image_rect.width/2
        self.image_y -= self.image_rect.height/2

        self.image_rect.x =self.image_x
        self.image_rect.y = self.image_y
        self.save = (self.image_rect.height/2)

        self.shadow_rect = self.shadow.get_rect()
        self.shadow_y = (y*coeff/2+self.save)
        self.shadow_rect.x = self.image_x
        self.shadow_rect.y = self.shadow_y

        # Booleans used to adapt the button to different situations.
        self.clicked = False
        self.was_pressed = False
        self.execute = False
        self.alt = state

    def Update(self, screen, button_choice, choice):
        action, check_levitation = False, False
        mouse_pos = pygame.mouse.get_pos()
        if self.y == 110*coeff:
            screen.blit(self.shadow,(self.image_x-coeff*self.multiplier,self.shadow_y-coeff*self.multiplier))
        elif self.y == 150*coeff:
            screen.blit(self.shadow,(self.image_x+coeff*self.multiplier,self.shadow_y-coeff*self.multiplier))
        else:
            screen.blit(self.shadow,(self.image_x+coeff*self.multiplier,self.shadow_y-coeff*self.multiplier))


        if button_choice == choice and not self.clicked:
            check_levitation = True
            self.increment += 0.25
            screen.blit(self.image,(self.image_x, self.image_y- 3*coeff - 4*math.sin(self.increment)))

        if self.image_rect.collidepoint(mouse_pos) or self.shadow_rect.collidepoint(mouse_pos):
            if not self.clicked and self.was_pressed and not self.alt and not check_levitation:
                self.increment += 0.25
                screen.blit(self.image,(self.image_x, self.image_y- 3*coeff - 4*math.sin(self.increment)))
            if self.alt:  
                if pygame.mouse.get_pressed()[0] == 0:
                    self.was_pressed = True
                else:
                    self.was_pressed = False
                self.alt = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        elif not check_levitation:
            screen.blit(self.image,(self.image_x, self.image_y))
            if pygame.mouse.get_pressed()[0] == 0:
                self.alt = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
            self.alt = True
            if self.image_rect.collidepoint(mouse_pos) or self.shadow_rect.collidepoint(mouse_pos):
                action= True
        if self.clicked and self.was_pressed:
            screen.blit(self.image1,(self.image_x, self.image_y))
        

        
        return action

    
def load_images(image,image1,shadow,multiplier):
    image = pygame.image.load(image).convert_alpha()
    image = scale(image, 'mult', coeff*multiplier)

    image1 = pygame.image.load(image1).convert_alpha()
    image1 = scale(image1, 'mult', coeff*multiplier)

    shadow = pygame.image.load(shadow).convert_alpha()
    shadow = scale(shadow, 'mult', coeff*multiplier)
    return image, image1,shadow

def create_animations(text,separation,x,y,mov,all_ani):
    if text == 'santa':
        y += coeff*6
    if text == 'indiana_jones':
        y += coeff*30
    elif text == 'adventurer':
        y += coeff*33
        x += coeff*2
    elif text == 'halo':
        y += coeff*33
    elif text == 'gladiator':
        x += coeff*5
        y += coeff*5
    elif text == 'dwarf':
        y += coeff*13
    elif text == 'hobbit':
        x -= coeff*3
        y += coeff*13
    elif text == 'hobbit':
        x -= coeff*3
        y += coeff*13
    hero_all_animations = [all_ani[heroes_dico[text][0]], heroes_dico[text][1], heroes_dico[text][2], text]
    return [Player([x+separation*coeff,y], hero_all_animations,mov)]

class cursor_heroes():
    def __init__(self,x,y,image):
        self.origin =x*coeff
        self.x = x*coeff
        self.y = y*2

        self.image = pygame.image.load("DWARF/Menu/"+image).convert_alpha()
        self.image = scale(self.image, 'mult', (coeff-0.5)*3)
        
        rect = self.image.get_rect()
        self.x -= rect.width/2
        self.y -= rect.height/2
        self.random = self.x
        self.x_move = 100*coeff
        self.y_move = separation_rows

        self.press_r = False
        self.press_l = False
        self.press_u = False
        self.press_d = False
        self.press_action = False
        
        self.stop_animation1 = False
        self.stop_animation2 = False 

        self.limit_right = 520*coeff
        self.limit_left = 130
        self.limit_up = 100*coeff
        self.limit_down = 380*coeff

        self.random
        
    def move_cursor(self,screen,idx, idy,stop_animations,idx2,idy2,acti,q_mark):
        react = False
        do_action = False
        action = 0
        keys = pygame.key.get_pressed()
        if acti == True:
            if keys[pygame.K_d] and self.press_r == False:
                self.press_r = True
            if self.press_r and not keys[pygame.K_d]:
                self.x += self.x_move
                idx += 1 
                react = True
                if self.x> self.limit_right or (idx == idx2 and idy == idy2):
                    self.x -= self.x_move
                    idx-= 1
                    react = False
                self.press_r= False
            
            if keys[pygame.K_q] and self.press_l == False:
                self.press_l = True
            if self.press_l and not keys[pygame.K_q]:
                self.x-= self.x_move
                idx -= 1
                react = True
                if self.x< self.limit_left or (idx == idx2 and idy == idy2):
                    self.x += self.x_move
                    idx+= 1
                    react = False
                self.press_l = False
            
            if keys[pygame.K_z] and not self.press_u:
                self.press_u = True
            if self.press_u and not keys[pygame.K_z]:
                self.y -= self.y_move
                idy -= 1
                react = True
                if self.y< self.limit_up or (idx == idx2 and idy == idy2):
                    self.y += self.y_move
                    idy+= 1
                    react = False
                self.press_u = False

            if keys[pygame.K_s] and not self.press_d:          
                self.press_d = True
            if self.press_d and not keys[pygame.K_s]:
                self.y += self.y_move
                idy += 1
                react = True
                if self.y> self.limit_down or (idx == idx2 and idy == idy2):
                    self.y -= self.y_move
                    idy-= 1
                    react = False
                self.press_d = False

        if keys[pygame.K_f] and not self.press_action:
            self.press_action = True
            stop_animations = not stop_animations
            acti = not acti
            pygame.mixer.Sound('DWARF/Sounds/shell.wav').play()

        if self.press_action and not keys[pygame.K_f]:
            action = 2
            react = True
            do_action = True
            self.press_action = False
        if q_mark:
            idx = randint(0,3)
            idy = randint(0,1)
            while(idx == idx2 and idy== idy2):
                idx = randint(0,3)
                idy = randint(0,1)
                
            self.x = self.x_move*idx + 420
            self.y = self.y_move*idy + 534
            react = True
            do_action = True
            q_mark = False
        if self.y > coeff*200:
            screen.blit(self.image,(self.x,self.y-coeff*22))
        else:
            screen.blit(self.image,(self.x,self.y))
        
        return react, action, idx, idy, do_action, stop_animations,acti,q_mark
    
    def move_cursor2(self,screen,idx, idy,stop_animations2,idx2,idy2,acti,q_mark):
        react = False
        do_action = False
        action = 0
        keys = pygame.key.get_pressed()
        if acti == True:
            if keys[pygame.K_m] and self.press_r == False:
                self.press_r = True
            if self.press_r and not keys[pygame.K_m]:
                self.x += self.x_move
                idx += 1 
                react = True
                if self.x> self.limit_right  or (idx == idx2 and idy == idy2):
                        self.x -= self.x_move
                        idx-= 1
                        react = False
                self.press_r= False
            
            if keys[pygame.K_k] and self.press_l == False:
                self.press_l = True
            if self.press_l and not keys[pygame.K_k]:
                self.x-= self.x_move
                idx -= 1
                react = True
                if self.x< self.limit_left or (idx == idx2 and idy == idy2):
                        self.x += self.x_move
                        idx+= 1
                        react = False
                self.press_l = False
            
            if keys[pygame.K_o] and not self.press_u:
                self.press_u = True
            if self.press_u and not keys[pygame.K_o]:
                self.y -= self.y_move
                idy -= 1
                react = True
                if self.y< self.limit_up or (idx == idx2 and idy == idy2):
                        self.y += self.y_move
                        idy+= 1
                        react = False   
                self.press_u = False

            if keys[pygame.K_l] and not self.press_d:          
                self.press_d = True
            if self.press_d and not keys[pygame.K_l]:
                self.y += self.y_move
                idy += 1
                react = True
                if self.y> self.limit_down or (idx == idx2 and idy == idy2):
                        self.y -= self.y_move
                        idy-= 1
                        react = False
                self.press_d = False

        if keys[pygame.K_CARET] and not self.press_action:
            self.press_action = True
            stop_animations2 = not stop_animations2
            acti = not acti
            pygame.mixer.Sound('DWARF/Sounds/shell.wav').play()
        if self.press_action and not keys[pygame.K_CARET]:
            action = 2
            react = True
            do_action = True
            self.press_action = False
            
        if q_mark:
            idx = randint(0,3)
            idy = randint(0,1)
            while(idx == idx2 and idy == idy2):
                idx = randint(0,3)
                idy = randint(0,1)
            
            self.x = self.x_move*idx + 420
            self.y = self.y_move*idy + 534
            react = True
            do_action = True
            q_mark = False

        if self.y > coeff*200:
            screen.blit(self.image,(self.x,self.y-coeff*22))
        else:
            screen.blit(self.image,(self.x,self.y))
        
        return react, action, idx, idy, do_action, stop_animations2,acti,q_mark

def generate(list_of_herosx,separation,all_ani):
    y = 0
    k = 0
    ctr = 0
    for o in range(4):
        list_of_herosx.append(create_animations(hero_list[o],separation,x_cord*coeff,y_cord,0,all_ani))
        separation+=100
    separation = 0
    for q in range(4):
        list_of_herosx.append(create_animations(hero_list[q+4],separation,x_cord*coeff,y_cord + separation_rows,0,all_ani))
        separation+=100
    return list_of_herosx

def show_selection(index_pos,indey_pos,move,detect,stop_animation,listx,list_heroes,hero_list, all_ani):
    y =0
    k= 0
    ctr = 0
    select = "none"
    for i in range(len(hero_list)):
        if(i >= 4):
            ctr = 1
            y = separation_rows
            k = i - 4
        else:
            k = i
        if (index_pos == k and indey_pos == ctr):
            move = 1
            if(detect and stop_animation):
                move = 2
                select = hero_list[i]
            list_heroes[i] = create_animations(hero_list[i],100*k,x_cord*coeff,y_cord+y,move,all_ani)
        else:
            listx.append(hero_list[i])
            
    return listx, list_heroes,select

class selection_of_characters():
    def __init__(self,all_ani):
        self.separation = 0
        self.all_animations = all_ani

        self.hero_list = ['santa','indiana_jones','adventurer','halo','dwarf','gladiator','hobbit','question_mark']
        self.list_of_heros = []
        self.list_of_heros = generate(self.list_of_heros,self.separation,self.all_animations)
       

        # Cursor 1
        self.move = 0
        self.detect = False
        self.cursor = cursor_heroes(x_cord+15,y_cord-5,"P1_cursor.png")
        self.index_pos = 0
        self.indey_pos = 0
        self.detect = False
        self.stop_animation = False
        self.selection1 = "none"
        self.activate = True
        self.listb = [] 
        self.sel_rand = False

        # Cursor 2
        self.move_2 = 0
        self.cursor2 = cursor_heroes(x_cord+115,y_cord-5,"P2_cursor.png")
        self.index_pos2 = 1
        self.indey_pos2 = 0
        self.detect2 =False
        self.stop_animation2 = False
        self.selection2 = "none"
        self.activate2 = True
        self.lista = [] 
        self.sel_rand2 = False

        self.listc = []


        
        self.cursor1_react = True
        self.cursor2_react = True
        self.a = True
    def create_selection(self,screen):
        self.cursor2_react, self.move_2, self.index_pos2, self.indey_pos2,self.detect2,self.stop_animation2,self.activate2,self.sel_rand2 = self.cursor2.move_cursor2(screen,self.index_pos2, self.indey_pos2,self.stop_animation2,self.index_pos,self.indey_pos,self.activate2,self.sel_rand2)
        self.cursor1_react, self.move, self.index_pos, self.indey_pos, self.detect, self.stop_animation, self.activate, self.sel_rand = self.cursor.move_cursor(screen, self.index_pos, self.indey_pos, self.stop_animation, self.index_pos2, self.indey_pos2, self.activate, self.sel_rand)
        if self.a == True:
            self.cursor1_react = True
            self.cursor2_react = True
            self.a =False

        if self.cursor1_react:
        
            self.listb = []
            self.listb, self.list_of_heros,self.selection1 = show_selection(self.index_pos,self.indey_pos,self.move,self.detect,self.stop_animation,self.listb,self.list_of_heros,self.hero_list,self.all_animations) 
            if (self.selection1 == 'question_mark'):
                self.sel_rand = True
            

        if self.cursor2_react:
            self.lista = [] 
            self.lista, self.list_of_heros, self.selection2 = show_selection(self.index_pos2,self.indey_pos2,self.move_2,self.detect2,self.stop_animation2,self.lista,self.list_of_heros,self.hero_list,self.all_animations)
            
            if (self.selection2 == 'question_mark'):
                self.sel_rand2 = True
            
        if self.cursor2_react or self.cursor1_react:
            self.listc=[]
            if self.listb == []:
                self.listc = self.lista
            elif self.lista == []:
                self.listc = self.listb
            
            for x in range(len(self.lista)):
                if(self.lista[x] in self.listb):
                    self.listc.append(self.lista[x])
            
            for element in self.listc:
                y =0
                k= 0
                ctr = 0
                for l in range(len(self.hero_list)):
                    
                    if(l >= 4):
                        ctr = 1
                        y = separation_rows
                        k = l - 4
                    else:
                        k = l
                    if element == self.hero_list[l]:
                        self.list_of_heros[l] = create_animations(element,100*k,x_cord*coeff,y_cord+y,0,self.all_animations)

            self.cursor1_react = False
            self.cursor2_react = False
        for self.list_of_animations in self.list_of_heros:
            for player1 in self.list_of_animations:
                player1.update(screen)
        
        return self.selection1,self.selection2, self.index_pos, self.indey_pos, self.index_pos2, self.indey_pos2
    
def show_data(screen,x,y,index,indey,nb_player):
    
    width_health = 0
    if nb_player == 1:
        stats_x = x + 116
        color = (253, 230, 97)
        shadow_color = (254,174,52)
    else:
        stats_x = x + 32
        color = (190, 119, 217)
        shadow_color = (122,85,146)

    shadow = pygame.Surface((210, 11), pygame.SRCALPHA)
    shadow.fill((0,0,0))
    shadow.set_alpha(50)
    
    if(index == 0 and indey == 0):
        width_health = santa_stats['health']
        width_speed = 2
        width_attack = santa_stats['attack']
        width_speed_attack = santa_stats['attack_speed']
        hero = "Santa"
    elif(index ==0 and indey ==1):
        width_health = dwarf_stats['health']
        width_speed = 12
        width_attack = dwarf_stats['attack']
        width_speed_attack = dwarf_stats['attack_speed']
        hero = "Dwarf"
    elif(index ==1 and indey ==0):
        width_health = indiana_jones_stats['health']
        width_speed = 9
        width_attack = indiana_jones_stats['attack']
        width_speed_attack = indiana_jones_stats['attack_speed']
        hero = "Indiana Jones"
    elif(index ==1 and indey ==1):
        width_health = gladiator_stats['health']
        width_speed = 6
        width_attack = gladiator_stats['attack']
        width_speed_attack = gladiator_stats['attack_speed']
        hero = "Gladiator"
    elif(index ==2 and indey ==0):
        width_health = adventurer_stats['health']
        width_speed = 13
        width_attack = adventurer_stats['attack']
        width_speed_attack = adventurer_stats['attack_speed']
        hero = "Adventurer"
    elif(index ==2 and indey ==1):
        width_health = hobbit_stats['health']
        width_speed = 13
        width_attack = hobbit_stats['attack']
        width_speed_attack = hobbit_stats['attack_speed']
        hero = "Hobbit"
    elif(index ==3 and indey ==0):
        width_health = halo_stats['health']
        width_speed = 8
        width_attack = halo_stats['attack']
        width_speed_attack = halo_stats['attack_speed']
        hero = "Halo"
    elif(index ==3 and indey ==1):
        width_health = 0
        width_speed = 0
        width_attack = 0
        width_speed_attack = 0
        hero = "?"


    screen.blit(scale(pygame.image.load(f'DWARF/Menu/p{str(nb_player)}_stats.png').convert_alpha(), 'mult', coeff*3.5), (x,y))

    screen.blit(shadow,(stats_x, y+168+21))
    pygame.draw.rect(screen, color, pygame.Rect(stats_x, (coeff/3)*(y+168), 210*width_health/max_stats['health'], 32))
    pygame.draw.rect(screen, shadow_color, pygame.Rect(stats_x, (coeff/3)*(y+168+21), 210*width_health/max_stats['health'], 11))
    
    screen.blit(shadow,(stats_x, y+168+126+21))
    pygame.draw.rect(screen, color, pygame.Rect(stats_x, (coeff/3)*(y+168+126), 210*width_speed/13, 32))
    pygame.draw.rect(screen, shadow_color, pygame.Rect(stats_x, (coeff/3)*(y+168+126+21), 210*width_speed/13, 11))
    
    screen.blit(shadow,(stats_x, y+168+126*2+21))
    pygame.draw.rect(screen, color, pygame.Rect(stats_x, (coeff/3)*(y+168+126*2), 210*width_attack/max_stats['attack'], 32))
    pygame.draw.rect(screen, shadow_color, pygame.Rect(stats_x, (coeff/3)*(y+168+126*2+21), 210*width_attack/max_stats['attack'], 11))
    
    screen.blit(shadow,(stats_x, y+168+126*3+21))
    pygame.draw.rect(screen, color, pygame.Rect(stats_x, (coeff/3)*(y+168+126*3), 210*width_speed_attack/max_stats['attack_speed'], 32))
    pygame.draw.rect(screen, shadow_color, pygame.Rect(stats_x, (coeff/3)*(y+168+126*3+21), 210*width_speed_attack/max_stats['attack_speed'], 11))
    