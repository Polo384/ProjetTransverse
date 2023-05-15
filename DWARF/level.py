import pygame, random
from tiles import *
from settings import player1_pos, player2_pos
from functions import *
from player import Player
from bonus import Bonus
from backgrounds import BG
from hud import *
from math import *

class Level:
    def __init__(self, level_data, surface, player1_hero, player2_hero):
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.players_list = [Player(1,player1_pos,player1_hero), Player(2,player2_pos,player2_hero)]
        self.bonus_group = pygame.sprite.GroupSingle()
        self.timer, self.timer_check = 0, True
        background_choice = random.randint(1,2)
        self.backgrounds_group = pygame.sprite.Group()
        self.backgrounds_group.add(BG(background_choice,1),BG(background_choice,2),BG(background_choice,3))
        self.hud_list = [HUD(self.players_list[0], self.players_list[0].hero_choice, 1), HUD(self.players_list[1], self.players_list[1].hero_choice, 2)]
        self.win = WIN(self.players_list)

        # Music
        self.music = pygame.mixer.Sound(f'DWARF/Musics/fight{str(random.randint(1,3))}.wav')
        self.music.set_volume(0.4)
        self.music.play()

    def setup_level(self, level_data):
        self.collide_tiles = pygame.sprite.Group()
        self.semi_collide_tiles = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        # =========== level_data ADDONS ===========
        stone_list = []
        stone_occurrences = element_occurrences(level_data, 5)
        for temp in range(stone_occurrences):
            stone_list.append(str(random.randint(1,6)))

        grass_list = []
        grass_occurrences = element_occurrences(level_data, 4)
        for temp in range(grass_occurrences):
            grass_list.append((random.choice(['F','G1','G1','G1'])))

        water_level = 3
        # ==================================

        # ============== MAP ===============
        stone_index, grass_index = 0, 0
        y = 0
        for i in range(len(level_data)):
            x = 0
            for j in range(len(level_data[0])):

                # WATER
                if  y == (len(level_data)-water_level)  and  y != (len(level_data)):
                    tile = Tile(x,y,'Water/W1.png')
                    self.tiles.add(tile)
                elif y > (len(level_data)-water_level)  and  y != (len(level_data)):
                    tile = Tile(x,y,'Water/W2.png')
                    self.tiles.add(tile)


                # ROCK
                if level_data[i][j] == 1: # Collisions Blocks   

                    # Yellow Blocks
                    if (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Yellow_Rock_Block/UM.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif if_matrix(level_data, i, j, 1, 3, 3, 1) or if_matrix(level_data, i, j, 3, 1, 3, 1):
                        tile = Tile(x,y,'Yellow_Rock_Block/M.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)
                    
                    elif level_data[i][j+1] == 0 and level_data[i][j-1] == 1 and level_data[i+1][j] == 1 and level_data[i-1][j] == 1 and level_data[i-2][j] != 1 and level_data[i+1][j+1] != 0 or (level_data[i][j+1] == 4 and  level_data[i-2][j] == 0):
                        tile = Tile(x,y,'Yellow_Rock_Block/SR.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile) 


                    elif level_data[i][j+1] != 1 and level_data[i][j-1] == 1 and level_data[i-1][j] in (0,5,3,4) and level_data[i+1][j] == 1:
                        if level_data[i][j+1] == 2:
                            tile = Tile(x,y,'Yellow_Rock_Block/UM.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                            tile = Tile(x,y,'Yellow_Rock_Block/UCR+.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                        else:
                            tile = Tile(x,y,'Yellow_Rock_Block/UCR.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)

                    elif level_data[i][j+1] == 1 and level_data[i][j-1] != 1 and level_data[i-1][j] in (0,5,3,4) and level_data[i+1][j] == 1:
                        if level_data[i][j-1] == 2:
                            tile = Tile(x,y,'Yellow_Rock_Block/UM.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                            tile = Tile(x,y,'Yellow_Rock_Block/UCL+.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                        else:
                            tile = Tile(x,y,'Yellow_Rock_Block/UCL.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 0 or level_data[i][j+1] == 5 or level_data[i][j+1] == 4) and level_data[i][j-1] == 1 and level_data[i-1][j] == 1 and (level_data[i+1][j] == 1 or level_data[i+1][j] == 3):
                        if level_data[i-2][j] == 0 or level_data[i-2][j] == 4 or level_data[i-2][j] == 5:
                            tile = Tile(x,y,'Purple_Rock_Yellow_Rock/R.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                        else:
                            tile = Tile(x,y,'Purple_Rock_Ground/R.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)

                    elif level_data[i][j+1] == 1 and level_data[i][j-1] == 2 and level_data[i+1][j] and level_data[i-1][j] == 1:
                        tile = Tile_Specific(x,y,'Bridge/M.png', False, True, False, False)
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)
                        tile = Tile(x,y,'Purple_Rock_Ground/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif level_data[i][j+1] == 1 and (level_data[i][j-1] == 0 or level_data[i][j-1] == 2) and level_data[i-1][j] == 1 and (level_data[i+1][j] == 1 or level_data[i+1][j] == 3) or level_data[i+1][j-1] == 2:
                        if level_data[i-2][j] == 0 or level_data[i-2][j] == 4 or level_data[i-2][j] == 5 or level_data[i][j-1] == 2 :
                            tile = Tile(x,y,'Purple_Rock_Yellow_Rock/L.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                        else:
                            tile = Tile(x,y,'Purple_Rock_Ground/L.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                            
                    elif if_matrix(level_data, i, j,1,1,1,1) and level_data[i-1][j-1] == 1 and (level_data[i-1][j+1] == 0 or level_data[i-1][j+1] == 4 or level_data[i-1][j+1] == 5) or (level_data[i][j-2] == 3 and level_data[i][j+2] == 0 and level_data[i+1][j+1] == 1 and level_data[i+1][j+1] == 1 and level_data[i+2][j+2] == 1):
                        tile = Tile(x,y,'Yellow_Rock_Block/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif if_matrix(level_data, i, j,1,1,1,1) and level_data[i-1][j+1] == 1 and (level_data[i-1][j-1] == 0 or level_data[i-1][j-1] == 4 or level_data[i-1][j-1] == 5) or (level_data[i][j+1] == 3 and level_data[i-2][j-1] == 0):
                        tile = Tile(x,y,'Yellow_Rock_Block/R.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)
                    
                    elif level_data[i][j+1] == 0 and level_data[i][j-1] != 0 and level_data[i-1][j] == 3 and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Yellow_Rock_Block/UCR+.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    # Purple ks
                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 1 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1 and level_data[i+1][j-1] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Bottom_Bottom/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 1 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1 and level_data[i+1][j+1] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Bottom_Bottom/R.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif level_data[i][j-1] == 1 and level_data[i+1][j] == 0 and level_data[i-1][j] == 1 and (level_data[i][j+1] == 1 or level_data[i][j+1] == 2):
                        tile = Tile_Specific(x,y,'Purple_Rock_Round_Top_Top/M.png', False, True, False, False)
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 0:
                        tile = Tile_Specific(x,y,'Purple_Rock_Round_Top_Top/R.png', False, True, False, True)
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 0:
                        tile = Tile_Specific(x,y,'Purple_Rock_Round_Top_Top/L.png', False, True, True, False)
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 0 and level_data[i-1][j] == 0 and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Purple_Rock_Round_Top_Top/UPL.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)
                    
                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 0 and level_data[i-1][j] == 0 and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Purple_Rock_Round_Top_Top/UPR.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Purple_Rock_Ground/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)
                        
                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Purple_Rock_Ground/R.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    # Classic

                    else:
                        tile = Tile(x,y,'Yellow_Rock_Block/M.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)


                # BRIDGE
                elif level_data[i][j] == 2: # one-way collision blocks
                    if ((level_data[i][j+1] == 2 or level_data[i][j+1] == 1) and (level_data[i][j-1] == 2 or level_data[i][j-1] == 1) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0) :
                        tile = Tile_Specific(x,y,'Bridge/M.png', False, True, False, False)
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 2 or level_data[i][j+1] == 1) and level_data[i][j-1] == 0 and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0:
                        tile = Tile_Specific(x,y,'Bridge/L.png', False, True, False, False)
                        tile.rect.height -= 1*coeff
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)

                    elif level_data[i][j+1] == 0 and (level_data[i][j-1] == 2 or level_data[i][j-1] == 1) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0:
                        tile = Tile_Specific(x,y,'Bridge/R.png', False, True, False, False)
                        tile.rect.height -= 1*coeff
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)


                elif level_data[i][j] == 4 or level_data[i][j] == 5:# No collision Blocks
                    # Grass
                    if level_data[i][j] == 4:
                        if level_data[i][j-1] == 4 and level_data[i][j+1] != 4:
                            tile = Tile_special(x,y,'Grass/RC.png',[],0,1)
                            self.tiles.add(tile)
                        elif level_data[i][j-1] !=4 and level_data[i][j+1] == 4:
                            tile = Tile_special(x,y,'Grass/LC.png',[],0,1)
                            self.tiles.add(tile)
                        else:
                            tile = Tile_special(x,y,'Grass/',grass_list,grass_index,2)
                            self.tiles.add(tile)

                        if grass_index < grass_occurrences:
                            grass_index += 1
                        else:
                            grass_index = 0

                    # Stones
                    elif level_data[i][j] == 5:
                        tile = Tile_special(x,y,'Stone/S',stone_list,stone_index,2)
                        self.tiles.add(tile)
                        if stone_index < stone_occurrences:
                            stone_index += 1
                        else:
                            stone_index = 0
                x += 1
            y += 1

    def shell_collision(self):
        player1, player2 = self.players_list[0], self.players_list[1]

        for sprite in self.collide_tiles.sprites():
            if player1.shell and (sprite.rect.colliderect(player1.shell.rect) or player2.rect.colliderect(player1.shell.rect)):
                self.projectile_damage_player(player1.shell, 100, 33*(player1.attack*player1.attack_speed*player1.attack_boost/360))
                player1.projectile_explosion_x, player1.projectile_explosion_y = player1.shell.rect.centerx, player1.shell.rect.centery
                player1.explode_shell()
                explosion = pygame.mixer.Sound('DWARF/Sounds/shell.wav')
                explosion.set_volume(1.2)
                explosion.play()
                
            if player2.shell and (sprite.rect.colliderect(player2.shell.rect) or player1.rect.colliderect(player2.shell.rect)):
                self.projectile_damage_player(player2.shell, 100, 33*(player2.attack*player2.attack_speed*player2.attack_boost/360))
                player2.projectile_explosion_x, player2.projectile_explosion_y = player2.shell.rect.centerx, player2.shell.rect.centery
                player2.explode_shell()
                explosion = pygame.mixer.Sound('DWARF/Sounds/shell.wav')
                explosion.set_volume(1.2)
                explosion.play()
    

    def projectile_damage_player(self, projectile, range, damage):
        for player in self.players_list:
            xb, xa = projectile.rect.centerx, player.rect.centerx
            yb, ya = projectile.rect.centery, player.rect.centery

            if xb-xa < 0: flip = False
            else: flip = True

            distance = round(sqrt((xb - xa)**2+(yb-ya)**2))

            if distance <= 50:
                player.damage(damage,1,flip, True)

            elif (50 < distance <= range/2):
                player.damage(damage/4*2,1,flip, True)

            elif (range/2 < distance <= range/1.5):
                player.damage(damage/4*3,1,flip, True)

            elif range/1.5 < distance <= range:
                player.damage(damage,1/4,flip, True)

    def grenade_collision(self):
        for player in self.players_list:
            if player.grenade_timer > 15:
                self.projectile_damage_player(player.grenade, 200, 50*(player.attack*player.attack_boost/15))
                player.projectile_explosion_x, player.projectile_explosion_y = player.grenade.rect.centerx, player.grenade.rect.centery
                player.explode_grenade()
                explosion = pygame.mixer.Sound('DWARF/Sounds/grenade.wav')
                explosion.play()

    def grenade_collision_horizontal(self):
        for player in self.players_list:
            grenade = player.grenade
            check_semi_collide = True
            
            if grenade : 
                grenade.rect.x += int(grenade.direction.x*coeff/3)

                for sprite in self.collide_tiles.sprites():
                        if sprite.rect.colliderect(grenade.rect):
                            check_semi_collide = False

                            if grenade.direction.x > 0:
                                grenade.rect.right = sprite.rect.left
                                grenade.rotation_factor_value /= -1.01
                                grenade.direction.x /= -1.4

                            elif grenade.direction.x < 0:
                                grenade.rect.left = sprite.rect.right
                                grenade.rotation_factor_value /= -1.01
                                grenade.direction.x /= -1.4
                
                if check_semi_collide:
                    for sprite in self.semi_collide_tiles.sprites():
                        if sprite.rect.colliderect(grenade.rect):
                            if grenade.direction.y > 0 and grenade.direction_save.y > 0:
                                if grenade.direction.x > 0:
                                    grenade.rect.right = sprite.rect.left
                                    grenade.rotation_factor_value /= -1.01
                                    grenade.direction.x /= -1.4

                                elif grenade.direction.x < 0:
                                    grenade.rect.left = sprite.rect.right
                                    grenade.rotation_factor_value /= -1.01
                                    grenade.direction.x /= -1.4

    def grenade_collision_vertical(self):
        for player in self.players_list:
            check_semi_collide = True
            grenade = player.grenade

            if grenade : 
                grenade.apply_gravity()

                for sprite in self.collide_tiles.sprites():             
                    if grenade and sprite.rect.colliderect(grenade.rect):
                        check_semi_collide = False

                        if grenade.direction.y > 0:
                            grenade.rect.bottom = sprite.rect.top
                            grenade.apply_bounce()

                        elif grenade.direction.y < 0:
                            grenade.rect.top = sprite.rect.bottom
                            grenade.direction.y = 0

                if check_semi_collide:
                    for sprite in self.semi_collide_tiles.sprites():             
                        if grenade and sprite.rect.colliderect(grenade.rect):

                            if grenade.direction.y > 0 and grenade.direction_save.y > 0:
                                grenade.rect.bottom = sprite.rect.top
                                grenade.apply_bounce()
                    
    
    def horizontal_movement_collision(self):
        for player in self.players_list:
            check_semi_collide, player.slide_allowed, player.detect_wall_collision = True, False, False
            if not player.speed_fix_check : player.rect.x += int(player.direction.x * player.speed * player.speed_boost)
            else : player.rect.x += int(player.direction.x * coeff/3 * player.speed_boost)
            
            for sprite in self.collide_tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    check_semi_collide = False
                    if player.direction.x < 0 or (player.push > 0 and player.opponent_flip) :
                        player.opponent_flip = not player.opponent_flip
                        player.push /= 1.5

                        if player.wall_jump_left:
                            player.wall_collision = True
                            player.wall_jump_left, player.wall_jump_right = False, True
                        player.rect.left = sprite.rect.right
                        player.slide_allowed, player.detect_wall_collision = True, True
                    
                    elif player.direction.x > 0 or (player.push > 0 and not player.opponent_flip):
                        player.opponent_flip = not player.opponent_flip
                        player.push /= 1.5

                        if player.wall_jump_right:
                            player.wall_collision = True
                            player.wall_jump_left, player.wall_jump_right = True, False
                        player.rect.right = sprite.rect.left
                        player.slide_allowed, player.detect_wall_collision = True, True

            if check_semi_collide:
                for sprite in self.semi_collide_tiles.sprites():
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.x < 0 and not player.down_movement or (player.push > 0 and player.opponent_flip):
                            player.opponent_flip = not player.opponent_flip
                            player.push /= 1.5

                            if player.wall_jump_left:
                                player.wall_collision = True
                                player.wall_jump_left, player.wall_jump_right = False, True
                            player.rect.left = sprite.rect.right
                        elif player.direction.x > 0 and not player.down_movement or (player.push > 0 and not player.opponent_flip):
                            player.opponent_flip = not player.opponent_flip
                            player.push /= 1.5

                            if player.wall_jump_right:
                                player.wall_collision = True
                                player.wall_jump_left, player.wall_jump_right = True, False
                            player.rect.right = sprite.rect.left
                
    def vertical_movement_collision(self):
        for player in self.players_list:
            check_semi_collide = True
            player.apply_gravity()

            for sprite in self.collide_tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    check_semi_collide = False
                    if player.direction.y > 0:
                        player.player_on_ground, player.wall_collision, player.wall_jump_left, player.wall_jump_right = True, False, True, True
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.direction.y = 0
                        player.rect.top = sprite.rect.bottom

            if check_semi_collide:
                for sprite in self.semi_collide_tiles.sprites():
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.y > 0:
                            player.down_movement_allowed = True
                        if player.direction.y > 0 and not player.down_movement:
                            player.player_on_ground, player.wall_collision, player.wall_jump_left, player.wall_jump_right = True, False, True, True
                            player.rect.bottom = sprite.rect.top
                            player.direction.y = 0
                        elif player.direction.y < 0 :
                            player.direction.y = 0
                            player.rect.top = sprite.rect.bottom    
            
    def spawn_bonus(self):
        bonus_choice = random.choice(['speed','attack', 'attack_speed', 'health', 'resistance'])
        self.current_bonus = Bonus(bonus_choice)
        self.bonus_group.add(self.current_bonus)
    
    def bonus_collision(self, player):
        if (player.rect.colliderect(self.current_bonus.rect) or (player.shell and player.shell.rect.colliderect(self.current_bonus.rect) or player.grenade and player.grenade.rect.colliderect(self.current_bonus.rect)))and not player.dead:
            self.current_bonus.effect(player)
            self.bonus_group.remove(self.current_bonus)
            self.timer = 0 
            player.effect_ongoing = True
            pop_sound = pygame.mixer.Sound('DWARF/Sounds/pop.wav')
            pop_sound.set_volume(0.8)
            pop_sound.play()
        
    def bonus_update(self):
        if not self.bonus_group:
            self.timer += 0.1
            if self.timer_check:
                self.timer_stop = random.randint(55,70)
                self.timer_check = False
            if int(self.timer) == self.timer_stop:
                self.spawn_bonus()
        else:
            self.timer_check = True
            self.bonus_group.draw(self.display_surface)
            self.current_bonus.update()
            for player in self.players_list:
                self.bonus_collision(player)

    def fight(self):
        player1 = self.players_list[0]
        player2 = self.players_list[1]

        if player1.rect.colliderect(player2.attack_rect) and not player1.temp_invincibility:
            player1.damage( player2.attack, player2.attack_boost , player2.flip, False)
            hit_sound = pygame.mixer.Sound(f'DWARF/Sounds/hit{str(random.randint(1,4))}.wav')
            hit_sound.play()
        if player2.rect.colliderect(player1.attack_rect) and not player2.temp_invincibility:
            player2.damage( player1.attack, player1.attack_boost , player1.flip, False)
            hit_sound = pygame.mixer.Sound(f'DWARF/Sounds/hit{str(random.randint(1,4))}.wav')
            hit_sound.play()

    def run(self):
        # EVENTS
        events = pygame.event.get()

        # background
        self.backgrounds_group.update()
        self.backgrounds_group.draw(self.display_surface)

        # level tiles
        self.tiles.draw(self.display_surface)

        # player
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.fight()
        
        for player in self.players_list:
            if player.escape:
                return False, True
            
            player.handle_events(events)
            player.update(self.display_surface)
            player.clear_effects()
        
        for player in self.players_list:
            player.draw_projectile_explosion(self.display_surface)
        
        self.shell_collision()
        self.grenade_collision_horizontal()
        self.grenade_collision_vertical()
        self.grenade_collision()
        
        # bonus
        self.bonus_update()

        # HUD
        for player_hud in self.hud_list:
            player_hud.update(self.display_surface)

        self.win.update(self.display_surface)
        if not self.win.check_dead and not self.win.music_check:
            self.music.stop()
            pygame.mixer.Sound(f'DWARF/Sounds/win.wav').play()
        
        if self.win.create_level:
            pygame.mixer.Sound(f'DWARF/Sounds/pop.wav').play()

        return self.win.start, self.win.create_level