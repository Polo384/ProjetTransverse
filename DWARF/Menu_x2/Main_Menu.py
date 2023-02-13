import ctypes
from Menu_classes import*



ctypes.windll.user32.SetProcessDPIAware()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
MAIN_menu = Menu()
game_start_variable = True

while game_start_variable:

    game_start_variable = MAIN_menu.create_menu(screen,game_start_variable)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_start_variable = False

    pygame.display.update()
