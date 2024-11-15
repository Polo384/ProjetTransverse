import pygame
from settings import coeff
import numpy as np

# To expand or shrink an image
def scale(img, choice, multiplier):
    if choice == 'mult':
        img = pygame.transform.scale(img, (img.get_rect().width*multiplier, img.get_rect().height*multiplier))
    elif choice == 'div':
        img = pygame.transform.scale(img, (img.get_rect().width/multiplier, img.get_rect().height/multiplier))
    else:
        print(f'{choice} is an invalid choice, choose "up" or "down".')
    return img
    

# To get a custom mask from an image
def get_mask(img):
    mask = pygame.mask.from_surface(img)
    return mask


# To detect collision of 2 masks
def detect_collision(mask1, mask2, pos1, pos2):
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    else:
        return False


# ================== ANIMATIONS ==================

def store_spritesheets_v1_one(dico : dict):
    spritesheet_animation = []
    for key, value in dico.items():
        animation = []
        spritesheet = pygame.image.load('DWARF/Heroes/'+key).convert_alpha()
        spritesheet = scale(spritesheet,'mult',coeff)

        # Découper le spritesheet en frames
        frame_height = spritesheet.get_height() // value[0][0]
        frame_width = spritesheet.get_width() // max(value[1])
        for x in range(value[0][0]):
            animation = []
            for i in range(value[1][x]):
                animation.append(spritesheet.subsurface((i*frame_width, x*frame_height, frame_width, frame_height)))
            spritesheet_animation.append(animation)
    return spritesheet_animation

def store_spritesheets_v1(dico_list : list):
    all_animations = []
    for dico in dico_list:
        spritesheet_animation = []
        for key, value in dico.items(): #value is a list
            animation = []
            spritesheet = pygame.image.load('DWARF/Heroes/'+key).convert_alpha()
            spritesheet = scale(spritesheet,'mult',coeff)

            # Découper le spritesheet en frames
            frame_height = spritesheet.get_height() // value[0][0]
            frame_width = spritesheet.get_width() // max(value[1])
            for x in range(value[0][0]):
                animation = []
                for i in range(value[1][x]):
                    animation.append(spritesheet.subsurface((i*frame_width, x*frame_height, frame_width, frame_height)))
                spritesheet_animation.append(animation)
            all_animations.append(spritesheet_animation)
    return all_animations

def store_spritesheets_v2(dico_list : list):
    all_animations = []
    for dico in dico_list:
        for key, value in dico.items(): #value is a list
            spritesheet_animation = []
            for i in range(1,value[0][0]+1):
                animation = []
                for j in range(1,value[1][i-1]+1):
                    spritesheet = pygame.image.load('DWARF/Heroes/'+key+str(i)+'/'+str(j)+'.png').convert_alpha()
                    spritesheet = scale(spritesheet,'mult',coeff)
                    animation.append(spritesheet)
                spritesheet_animation.append(animation)
            all_animations.append(spritesheet_animation)
    return all_animations

# For multiple horizontal spritesheets
def store_spritesheets_v3(dico_list : list):
    all_animations = []
    for dico in dico_list:
        spritesheet_animation = []
        for key, value in dico.items():
            animation = []
            spritesheet = pygame.image.load('DWARF/Heroes/'+key).convert_alpha()
            spritesheet = scale(spritesheet,'mult',coeff)

            # Découper le spritesheet en frames
            frame_width = spritesheet.get_width() // value
            frame_height = spritesheet.get_height()
            for i in range(value):
                animation.append(spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height)))
            spritesheet_animation.append(animation)
        all_animations.append(spritesheet_animation)
    return all_animations

    
# Final function for animations
def store_animations(spritesheets_list_v1,spritesheets_list_v2):
    v1, v2 = store_spritesheets_v1(spritesheets_list_v1), store_spritesheets_v2(spritesheets_list_v2)
    for i in v2:
        v1.append(i)
    all_animations = v1
    return all_animations
    

def store_special_animations(list, path):
    all_animations = []
    for i in range(1, list[0][0]+1):
        animation = []
        for j in range(1,list[1][i-1]+1):
            spritesheet = pygame.image.load(f'DWARF/{path}/'+str(i)+'/'+str(j)+'.png').convert_alpha()
            spritesheet = scale(spritesheet,'mult',coeff)
            animation.append(spritesheet)
        all_animations.append(animation)
    return all_animations

# ===================== END =====================


def display_map(path, screen, x, y):
    screen.blit(scale(pygame.image.load('DWARF/Tiles/'+str(path)).convert_alpha(),'mult',2),(x*17*2-17*2,y*17*2-17*2))


# Return the number of occurences of an element in a list
def element_occurrences(list, element):
    cpt = 0
    for i in range(len(list)):
        for j in range(len(list[0])):
            if element == list[i][j]:
                cpt += 1
    return cpt

# If statement for the map matrix
def if_matrix(map, i, j, right,left,down,up):
    if map[i][j+1] == right and map[i][j-1] == left and map[i-1][j] == down and map[i+1][j] == up:
        return True
    else:
        return False
    

# Found on a blog on the internet, in order to render a B&W image :
def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.pixels3d(surface)
    mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
    mean_arr3d = mean_arr[..., np.newaxis]
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    image = pygame.surfarray.make_surface(new_arr)
    image.set_colorkey((0,0,0))

    return image


