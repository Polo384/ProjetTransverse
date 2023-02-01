import pygame, time, sys, ctypes
from functions import *

ctypes.windll.user32.SetProcessDPIAware() # To adapt to screen size

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.stamina = 10
        self.sprinting = False
        self.distance = 0
        if number == 1:
            self.velocity = 1
            self.image = pygame.image.load('DWARF/icon/icon.png').convert_alpha()
            self.image = scale(self.image,'div',10)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = 50
            self.rect.y = 50
            self.move_keys = {
                'up': pygame.K_UP,
                'down': pygame.K_DOWN,
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'sprint': pygame.K_RCTRL
            }
        elif number == 2:
            self.velocity = 2
            self.image = pygame.image.load('DWARF/icon/joris0.png').convert_alpha()
            self.image = scale(self.image,'div',5)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = 300
            self.rect.y = 300
            self.move_keys = {
                'up': pygame.K_z,
                'down': pygame.K_s,
                'left': pygame.K_q,
                'right': pygame.K_d,
                'sprint': pygame.K_LSHIFT
            }

    def reload_stamina(self):
        if self.stamina < 10:
            self.stamina += 0.03
    
    def use_stamina(self):
        if self.stamina > 0:
            self.stamina -= 0.04
    
    def sprint(self, keys):
        if keys[self.move_keys['sprint']] and self.stamina > 0.1:
            self.distance = 5*self.velocity
            self.use_stamina()
            self.sprinting = True
        elif keys[self.move_keys['sprint']] and self.stamina <= 0.1:
            self.sprinting = False
            self.use_stamina()
            self.distance = 1*self.velocity
        else:
            self.sprinting = False
            self.distance = 1*self.velocity
        return self.distance, self.sprinting

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[self.move_keys['up']]:
            self.distance, self.sprinting = self.sprint(keys)
            self.rect.y -= self.distance
        if keys[self.move_keys['down']]:
            self.distance, self.sprinting = self.sprint(keys)
            self.rect.y += self.distance
        if keys[self.move_keys['left']]:
            self.distance, self.sprinting = self.sprint(keys)
            self.rect.x -= self.distance
            print(self.distance)
        if keys[self.move_keys['right']]:
            self.distance, self.sprinting = self.sprint(keys)
            self.rect.x += self.distance
        # If player press sprint but does not move, his stamina reloads
        if keys[self.move_keys['sprint']] and not(keys[self.move_keys['up']]) and not(keys[self.move_keys['down']]) and not(keys[self.move_keys['left']]) and not(keys[self.move_keys['right']]):
            self.sprinting = False

    def update(self):
        self.move_player()
        if not self.sprinting:
            self.reload_stamina()

        # Display the stamina
        stamina_surface = pygame.Surface((self.stamina*20,30))
        stamina_surface.fill('Red')
        screen.blit(stamina_surface,(self.rect.x,self.rect.y-100))




# Initialisation
pygame.init()
test_font = pygame.font.Font(None, 50)
# Clock
clock = pygame.time.Clock()

# Create the screen
# screen = pygame.display.set_mode((1920,1080),pygame.SCALED)
screen = pygame.display.set_mode((800,400))

# Title and icon
pygame.display.set_caption('DWARF')
icon = pygame.image.load('DWARF/icon/icon.png')
pygame.display.set_icon(icon)

# Players
player_group = pygame.sprite.Group()
player_group.add(Player(1),Player(2))
players = player_group.sprites()

# Game loop
running = True
while running:
    clock.tick(60) # ralentir le jeu, donc ralentir le joueur, car on ne peut pas donner une distance inférieure à 1 pixel
    screen.fill((255,255,255))
    
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:   # Press k to exit (c'est utile pour moi j'ai le bouton k sur ma souris mdr)
                pygame.quit()
                sys.exit()

    # Player
    player_group.update()
    player_group.draw(screen)
    pygame.display.flip()
    # Collision detection
    if detect_collision(players[0].mask, players[1].mask, (players[0].rect.x,players[0].rect.y),(players[1].rect.x,players[1].rect.y)):
        print("Collision !")

    # Update
    pygame.display.update()