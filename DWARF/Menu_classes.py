import pygame
#from moviepy.editor import VideoFileClip
import math as math
from settings import screen_width, screen_height, FPS, level_map
#from pygame.locals import *
from functions import scale
from backgrounds import*




from Heroes_Dico import *
from functions import store_animations,scale
from Animation import*
from random import*
from level import Level
from Heroes_Dico import santa_stats
y_cord = 300
x_cord = 160
seed(57)
separation_rows = 400


hero_list = ['santa','indiana_jones','adventurer','halo','dwarf','gladiator','hobbit','question_mark']

# Classes

class Menu():
    def __init__(self,all_ani):
        
        self.title = None
        self.menu = 0

        self.confirm = -1

        self.y_coord = 130*coeff

        self.play = Buttons_2(screen_width/coeff, 100*coeff,5.5, "DWARF/Menu/play.png","DWARF/Menu/play_press.png","DWARF/Menu/play_shadow.png",True)
        self.quit = Buttons_2(screen_width/coeff, 200*coeff, 5.5,"DWARF/Menu/quit.png","DWARF/Menu/quit_pressed.png","DWARF/Menu/quit_shadow.png",True)
        self.options = Buttons_2(screen_width/coeff, 150*coeff, 5.5,"DWARF/Menu/options.png","DWARF/Menu/options_press.png","DWARF/Menu/options_shadow.png",True)

        # Title and sprites
        self.y = 35*coeff
        self.sin_increment = 0
        # music variables

        self.volume = 0.1
        self.background_music = window("DWARF", "DWARF/Musics/Menu2.wav", self.volume)
        self.play_music = True
        self.music_on = Sprites(5, 5,False, "DWARF/Menu/mute_on.png", 1)
        self.music_off = Sprites(5, 5,False, "DWARF/Menu/mute_off.png", 1)
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
    def create_menu(self, screen, game_start_variable):
        

        if self.menu == 0:
            self.create_level = False
            # PLays the video one time
            self.backgrounds_group.update()
            self.backgrounds_group.draw(screen)
            
            self.y += (math.sin(self.sin_increment) * 1)
            self.sin_increment += 0.1
            self.title = Sprites(screen_width/coeff, self.y,True, "DWARF/Menu/dwarf.png", 0.8)
            self.title.detect_click(screen)
            game_start_variable, self.y_coord, self.confirm = \
                self.cursor_main.cursor_menu(screen,100*coeff + (math.sin(self.sin_increment) * 10) ,self.y_coord, game_start_variable)
            if self.play.Update(screen) or self.confirm == 0:
                
                self.menu = 1
            if self.options.Update(screen) or self.confirm == 1:
                print("options")    
            if self.quit.Update(screen) or self.confirm == 2:
                game_start_variable = False
            self.Selections = selection_of_characters(self.all_ani)
            # Mute the sound
            if not self.mute:
                if self.music_on.detect_click(screen):
                    self.mute = True
                    self.background_music.set_volume(0)
            else:
                if self.music_off.detect_click(screen):
                    self.background_music.set_volume(self.volume)
                    self.mute = False

        elif self.menu == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.menu = 0
            self.menu = self.char_page.put(screen,self.menu)
            
            self.player1 , self.player2,self.pos_player1_x, self.pos_player1_y, self.pos_player2_x, self.pos_player2_y = self.Selections.create_selection(screen)
            show_data(screen,50,250,self.pos_player1_x, self.pos_player1_y,1)
            show_data(screen,1620,250,self.pos_player2_x, self.pos_player2_y,2)
            if(self.menu == 2 and (self.player1 == "none" or self.player2 == "none")):
                self.menu = 1
        elif self.menu == 2:
            self.create_level = True
            self.background_music.set_volume(0)

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


class Options:
    def __init__(self, image, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.pos = (x, y)


"""class Video:
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
            self.frame_iter = iter(self.video.iter_frames())"""


"""class LoadingBar:
    def __init__(self):
        self.bar = pygame.Rect((190, 200), (400, 100))
        self.width = 75
        self.increase = 1
        self.loading_bar = pygame.Rect((210, 212), (1, 75))

    def create_bar(self, screen):
        screen.fill((0, 0, 0))
        text_creation("Loading", (pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", 75)), (255, 255, 255), 280, 100, screen)
        pygame.draw.rect(screen, (255, 255, 255), self.bar, 5, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), self.loading_bar, border_radius=2)
        if self.loading_bar.width < 360:
            self.increase += 0.05
            self.loading_bar.width = self.width + self.increase"""


class Sprites(pygame.sprite.Sprite):
    def __init__(self, x, y,take_center, image, multiplier):
        super().__init__()
        self.image = pygame.image.load(image)
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
        self.separation = 72*coeff
    def cursor_menu(self,screen, x, y, game_start_variable):
        image = pygame.image.load("DWARF/Menu/cursor.png")
        image = scale(image, 'mult', coeff*2)
        keys = pygame.key.get_pressed()
        select = -1
        
        if keys[pygame.K_DOWN] and self.pressed_down == False:
                self.pressed_down = True
        if self.pressed_down and not keys[pygame.K_DOWN]:
            y += self.separation
            if(y> 274*coeff):
                y -= self.separation
            self.pressed_down = False

        if keys[pygame.K_UP] and self.pressed_up == False:
                self.pressed_up = True
        if self.pressed_up and not keys[pygame.K_UP] :
            y -= self.separation
            if(y< 130*coeff):
                y+= self.separation
            self.pressed_up = False    

        if (y == 390) and keys[pygame.K_SPACE]:
            select = 0
        elif (y == 606) and keys[pygame.K_SPACE] :
            select = 1 
        elif(y == 822) and keys[pygame.K_SPACE]:
            select = 2  
        
        screen.blit(image, (x, y))

        return game_start_variable, y, select


class page_characters:
    def __init__(self):
        self.x = 150

        self.herostext_font = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", int(30*coeff/2))
        self.fonts = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", int(75*coeff/2))

        self.back_char = pygame.image.load("DWARF/Menu/tabern.jpg")
        self.back_char = scale(self.back_char, 'mult', coeff/3)

        self.y = 45
        self.sin_increment = 0
        self.back = Buttons("Back",20*coeff/2,425*coeff/2,120,60,True,50,12,(83,11,20))
        self.play_game= Buttons("Play",750*coeff/2,425*coeff/2,120,60,True,50,12,(11,83,29))

    def put(self, screen,menu):
        screen.blit(self.back_char, (0, 0))
        self.y += round(math.sin(self.sin_increment)*1)
        self.sin_increment += 0.1
        text_creation("Select your Hero", self.fonts, (255, 255, 255), screen_width/2, self.y,True, screen)
        keys = pygame.key.get_pressed()
    
        if self.play_game.draw(screen) or keys[pygame.K_SPACE]:
            menu = 2
        if self.back.draw(screen):
            menu = 0

        
        return menu


class Buttons_2():
    def __init__(self, x, y, multiplier, image, image1, shadow, state):

        #Loads images and gets their center coordenates
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
    def Update(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self.shadow,(self.image_x-15,self.shadow_y-15))
        if self.image_rect.collidepoint(mouse_pos) or self.shadow_rect.collidepoint(mouse_pos):
            if not self.clicked and self.was_pressed and not self.alt:
                screen.blit(self.image,(self.image_x, self.image_y-5*coeff/2))
            if self.alt:  
                if pygame.mouse.get_pressed()[0] == 0:
                    self.was_pressed = True
                else:
                    self.was_pressed = False
                self.alt = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
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
        else:
            screen.blit(self.image,(self.image_x, self.image_y))

        
        return action

    
def load_images(image,image1,shadow,multiplier):
    image = pygame.image.load(image,image1,)
    image = scale(image, 'mult', coeff*multiplier)

    image1 = pygame.image.load(image1)
    image1 = scale(image1, 'mult', coeff*multiplier)

    shadow = pygame.image.load(shadow)
    shadow = scale(shadow, 'mult', coeff*multiplier)
    return image, image1,shadow

def create_animations(text,separation,x,y,mov,all_ani):
    if(text == 'santa'):
        y-=60
    hero_all_animations = [all_ani[heroes_dico[text][0]], heroes_dico[text][1], heroes_dico[text][2], text]
    return [Player([x+separation*coeff,y], hero_all_animations,mov)]

class cursor_heroes():
    def __init__(self,x,y,image):
        self.origin =x*coeff
        self.x = x*coeff
        
        self.y = y*2

        self.image = pygame.image.load("DWARF/Menu/"+image)
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
            if keys[pygame.K_RIGHT] and self.press_r == False:
                self.press_r = True
            if self.press_r and not keys[pygame.K_RIGHT]:
                self.x += self.x_move
                idx += 1 
                react = True
                if self.x> self.limit_right or (idx == idx2 and idy == idy2):
                    self.x -= self.x_move
                    idx-= 1
                    react = False
                self.press_r= False
            
            if keys[pygame.K_LEFT] and self.press_l == False:
                self.press_l = True
            if self.press_l and not keys[pygame.K_LEFT]:
                self.x-= self.x_move
                idx -= 1
                react = True
                if self.x< self.limit_left or (idx == idx2 and idy == idy2):
                    self.x += self.x_move
                    idx+= 1
                    react = False
                self.press_l = False
            
            if keys[pygame.K_UP] and not self.press_u:
                self.press_u = True
            if self.press_u and not keys[pygame.K_UP]:
                self.y -= self.y_move
                idy -= 1
                react = True
                if self.y< self.limit_up or (idx == idx2 and idy == idy2):
                    self.y += self.y_move
                    idy+= 1
                    react = False
                self.press_u = False

            if keys[pygame.K_DOWN] and not self.press_d:          
                self.press_d = True
            if self.press_d and not keys[pygame.K_DOWN]:
                self.y += self.y_move
                idy += 1
                react = True
                if self.y> self.limit_down or (idx == idx2 and idy == idy2):
                    self.y -= self.y_move
                    idy-= 1
                    react = False
                self.press_d = False

        if keys[pygame.K_RCTRL] and not self.press_action:
            self.press_action = True
            stop_animations = not stop_animations
            acti = not acti
        if self.press_action and not keys[pygame.K_RCTRL]:
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
        screen.blit(self.image,(self.x,self.y))
        
        return react, action, idx, idy, do_action, stop_animations,acti,q_mark
    
    def move_cursor2(self,screen,idx, idy,stop_animations2,idx2,idy2,acti,q_mark):
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
                if self.x> self.limit_right  or (idx == idx2 and idy == idy2):
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
            stop_animations2 = not stop_animations2
            acti = not acti
        if self.press_action and not keys[pygame.K_f]:
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
    hero = "none"
    font = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", 40)
    if(index == 0 and indey == 0):
        width_health = santa_stats['health']
        width_speed = santa_stats['speed']
        width_attack = santa_stats['attack']
        width_speed_attack = santa_stats['attack_speed']
        hero = "Santa"
    elif(index ==0 and indey ==1):
        width_health = dwarf_stats['health']
        width_speed = dwarf_stats['speed']
        width_attack = dwarf_stats['attack']
        width_speed_attack = dwarf_stats['attack_speed']
        hero = "Dwarf"
    elif(index ==1 and indey ==0):
        width_health = indiana_jones_stats['health']
        width_speed = indiana_jones_stats['speed']
        width_attack = indiana_jones_stats['attack']
        width_speed_attack = indiana_jones_stats['attack_speed']
        hero = "Indiana Jones"
    elif(index ==1 and indey ==1):
        width_health = gladiator_stats['health']
        width_speed = gladiator_stats['speed']
        width_attack = gladiator_stats['attack']
        width_speed_attack = gladiator_stats['attack_speed']
        hero = "Gladiator"
    elif(index ==2 and indey ==0):
        width_health = adventurer_stats['health']
        width_speed = adventurer_stats['speed']
        width_attack = adventurer_stats['attack']
        width_speed_attack = adventurer_stats['attack_speed']
        hero = "Adventurer"
    elif(index ==2 and indey ==1):
        width_health = hobbit_stats['health']
        width_speed = hobbit_stats['speed']
        width_attack = hobbit_stats['attack']
        width_speed_attack = hobbit_stats['attack_speed']
        hero = "Hobbit"
    elif(index ==3 and indey ==0):
        width_health = halo_stats['health']
        width_speed = halo_stats['speed']
        width_attack = halo_stats['attack']
        width_speed_attack = halo_stats['attack_speed']
        hero = "Halo"
    elif(index ==3 and indey ==1):
        width_health = 0
        width_speed = 0
        width_attack = 0
        width_speed_attack = 0
        hero = "Random"    

    font2 = pygame.font.Font("DWARF/Menu/ThaleahFat.ttf", 60)
    text_creation('PLAYER '+str(nb_player)+':', font2, (255, 255, 255), x, y,False, screen)

    text_creation(hero+' :', font, (255, 255, 255), x, y+75,False, screen)
    pygame.draw.rect(screen, (230,230,230), pygame.Rect(x,(coeff/3)*(y+200), 200 , 5*coeff*5/3))
    pygame.draw.rect(screen, (206,76,76), pygame.Rect(x, (coeff/3)*(y+200), 200*width_health/max_stats['health'], 5*coeff*5/3))
    text_creation('Health', font, (255, 255, 255), x, y+150,False, screen)
    pygame.draw.rect(screen, (230,230,230), pygame.Rect(x, (coeff/3)*(y+290), 200 , 5*coeff*5/3))
    pygame.draw.rect(screen, (75,175,194), pygame.Rect(x, (coeff/3)*(y+290), 200*width_speed/max_stats['speed'], 5*coeff*5/3))
    text_creation('Speed', font, (255, 255, 255), x,y+240,False, screen)

    pygame.draw.rect(screen, (230,230,230), pygame.Rect(x, (coeff/3)*(y+380), 200 , 5*coeff*5/3))
    pygame.draw.rect(screen, (135, 142, 141), pygame.Rect(x, (coeff/3)*(y+380), 200*width_attack/max_stats['attack'], 5*coeff*5/3))
    text_creation('Attack', font, (255, 255, 255), x, y+330,False, screen)

    pygame.draw.rect(screen, (230,230,230), pygame.Rect(x, (coeff/3)*(y+470), 200 , 5*coeff*5/3))
    pygame.draw.rect(screen, (255, 255, 47), pygame.Rect(x, (coeff/3)*(y+470), 200*width_speed_attack/max_stats['attack_speed'], 5*coeff*5/3))
    text_creation('Speed Attack', font, (255, 255, 255), x, y+420,False, screen)
