import pygame
import random
from comet_event import *
import animation

#Créer classe du joueur
class Player(animation.AnimateSprite):

    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 20
        self.velocity = 2
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500
    
    def dammage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            #Si le joueur a 0 pv
            self.game.game_over()

    def update_animation(self):
        self.animate()
    
    def update_health_bar(self, surface):
        #dessiner barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 7])

    def launch_projectile(self):
        #Créer instance de classe projectile
        self.all_projectiles.add(Projectile(self))
        #démarrer anim
        self.start_animation()

    def move_right(self):
        #si le joueur ne rentre pas en collision avec un monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
    
    def move_left(self):
        self.rect.x -= self.velocity


#Créer classe pour le jeu
class Game:

    def __init__(self):
        #définir si le jeu a commencé
        self.is_playing = False
        #générer joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #générer event
        self.comet_event = CometFallEvent(self)
        #groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}
        
    
    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()


    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)
    
    def game_over(self):
        #remettre le jeu à 0 : retirer les mobs etc...
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
    
    def update(self, screen):
        #Appliquer joueur
        screen.blit(self.player.image, self.player.rect)

        #Actualiser barre de vie joueur
        self.player.update_health_bar(screen)

        #Actualiser l'animation du joueur
        self.player.update_animation()

        #Actualiser barre d'event
        self.comet_event.update_bar(screen)

        #Récupérer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        #Récuperer les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
        
        #Récupérer les comètes du jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        #Appliquer projectile
        self.player.all_projectiles.draw(screen)

        #Appliquer les images des monstres
        self.all_monsters.draw(screen)

        #Appliquer ensemble image du groupe de comètes
        self.comet_event.all_comets.draw(screen)
    
        #vérifier dans quel sens on veut aller
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()


#Créer classe du projectile
class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 3
        self.player =player
        self.image = pygame.image.load("PygameAssets-main/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        #tourner projectile
        self.angle += 3
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        #suppr le projectile
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        #Vérifier si le projectile touche un monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            #suppr proj
            self.remove()
            #infliger des degats
            monster.dammage(self.player.attack)

        #vérifier si le projectile sort de la fenêtre (et le suppr)
        if self.rect.x > 1080:
            self.remove()

#Créer classe du monstre
class Monster(animation.AnimateSprite):

    def __init__(self, game):
        super().__init__("mummy")
        self.game = game
        self.health = 100
        self.max_health = 100
        self.velocity = random.random() 
        self.attack = 0.1
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540
        self.start_animation()

    def dammage(self, amount):
        #infliger dégats
        self.health -= amount

        #vérifier le nouveau nombre de point de vie
        if self.health <= 0:
            #faire réapparaitre le monstre comme si il était nouveau
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.random() + random.random()
            self.health = self.max_health

            #si l'event comète est actif
            if self.game.comet_event.is_full_loaded():
                #retirer du jeu
                self.game.all_monsters.remove(self)
                
                #Essayer de déclencher pluie
                self.game.comet_event.attempt_fall()

    def update_animation(self):
        self.animate(loop = True)

    def update_health_bar(self, surface):
        #dessiner barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])
        

    def forward(self):
        #Déplacement si il n'y a pas de collision avec le groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        #si le monstre touche le joueur
        else:
            #infliger des degats
            self.game.player.dammage(self.attack)