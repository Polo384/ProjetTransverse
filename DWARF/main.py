import pygame, ctypes, sys
from functions import *
from settings import *
from level import Level
from Heroes_Dico import *
ctypes.windll.user32.SetProcessDPIAware() # To adapt to screen size

# Setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED)
clock = pygame.time.Clock()
icon = pygame.image.load('DWARF/icon/icon.png')
pygame.display.set_icon(icon)

all_animations = store_animations([santa_dico_v1, minotaur_dico_v1,dwarf_dico_v1, indiana_jones_dico_v1, adventurer_dico_v1, bat_dico_v1, halo_dico_v1,gladiator_dico_v1, demon_dico_v1, cyclop_dico_v1],[hobbit_dico_v2],[skeleton_dico_v3])

player1_hero_choice = 'santa'
player2_hero_choice = 'indiana_jones'

player1_hero = [  all_animations[heroes_dico[player1_hero_choice][0]]  ,  heroes_dico[player1_hero_choice][1]  ,  heroes_dico[player1_hero_choice][2]  ]
player2_hero = [  all_animations[heroes_dico[player2_hero_choice][0]]  ,  heroes_dico[player2_hero_choice][1]  ,  heroes_dico[player2_hero_choice][2]  ]

level = Level(level_map, screen, player1_hero, player2_hero)
# Game loop
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:   # Press k to exit (c'est utile pour moi j'ai le bouton k sur ma souris mdr)
                    pygame.quit()
                    sys.exit()

    screen.fill('white')
    level.run()
    
    pygame.display.update()
    clock.tick(FPS)