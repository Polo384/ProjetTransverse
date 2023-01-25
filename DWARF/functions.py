import pygame


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


# To cut spritesheet
def cut_spritesheet(spritesheet, number_of_frames):
    # Cut image in the number of frames
    frame_width = spritesheet.get_width() // number_of_frames
    frame_height = spritesheet.get_height()
    frames = []
    for i in range(number_of_frames):
        frames.append(spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height)))
    return frames


def store_spricesheets(dico_list):
    all_animations = []
    for dico in dico_list:
        spricesheet_animation = []
        for key, value in dico.items():
            animation = []
            spritesheet = pygame.image.load('DWARF/Heroes/'+key)
            spritesheet = scale(spritesheet,'mult',10)

            # Découper le spritesheet en 8 frames
            frame_width = spritesheet.get_width() // value
            frame_height = spritesheet.get_height()
            for i in range(value):
                animation.append(spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height)))
            spricesheet_animation.append(animation)
        all_animations.append(spricesheet_animation)
    return all_animations