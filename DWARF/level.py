import pygame, random
from tiles import Tile, Tile_special
from settings import player1_pos, player2_pos
from functions import *
from player import Player
from bonus import Bonus
from backgrounds import BG
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
                if  y == (len(level_data)-water_level)  and  y != (len(level_data)-1):
                    tile = Tile(x,y,'Water/W1.png')
                    self.tiles.add(tile)
                elif y > (len(level_data)-water_level)  and  y != (len(level_data)-1):
                    tile = Tile(x,y,'Water/W2.png')
                    self.tiles.add(tile)


                # ROCK
                if level_data[i][j] == 1: # Collisions Blocks                    
                    # Yellow Blocks
                    if (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 1:
                        tile = Tile(x,y,'Yellow_Rock_Block/UM.png')
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

                    elif level_data[i][j+1] == 1 and level_data[i][j-1] == 0 and level_data[i-1][j] == 1 and (level_data[i+1][j] == 1 or level_data[i+1][j] == 3):
                        if level_data[i-2][j] == 0 or level_data[i-2][j] == 4 or level_data[i-2][j] == 5:
                            tile = Tile(x,y,'Purple_Rock_Yellow_Rock/L.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                        else:
                            tile = Tile(x,y,'Purple_Rock_Ground/L.png')
                            self.tiles.add(tile)
                            self.collide_tiles.add(tile)
                            
                    elif if_matrix(level_data, i, j,1,1,1,1) and level_data[i-1][j-1] == 1 and (level_data[i-1][j+1] == 0 or level_data[i-1][j+1] == 4 or level_data[i-1][j+1] == 5):
                        tile = Tile(x,y,'Yellow_Rock_Block/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif if_matrix(level_data, i, j,1,1,1,1) and level_data[i-1][j+1] == 1 and (level_data[i-1][j-1] == 0 or level_data[i-1][j-1] == 4 or level_data[i-1][j-1] == 5):
                        tile = Tile(x,y,'Yellow_Rock_Block/R.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)


                    # Purple ks
                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 1 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1 and level_data[i+1][j-1] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Bottom_Bottom/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 1 and level_data[i-1][j] == 1 and level_data[i+1][j] == 1 and level_data[i+1][j+1] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Bottom_Bottom/L.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif if_matrix(level_data, i, j,1,1,1,0):
                        tile = Tile(x,y,'Purple_Rock_Round_Top_Top/M.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j-1] == 1 or level_data[i][j-1] == 3) and level_data[i][j+1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Top_Top/R.png')
                        self.tiles.add(tile)
                        self.collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 1 or level_data[i][j+1] == 3) and level_data[i][j-1] == 0 and level_data[i-1][j] == 1 and level_data[i+1][j] == 0:
                        tile = Tile(x,y,'Purple_Rock_Round_Top_Top/L.png')
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
                    if (level_data[i][j+1] == 2 or level_data[i][j+1] == 1) and (level_data[i][j-1] == 2 or level_data[i][j-1] == 1) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0:
                        tile = Tile(x,y,'Bridge/M.png')
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)

                    elif (level_data[i][j+1] == 2 or level_data[i][j+1] == 1) and level_data[i][j-1] == 0 and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0:
                        tile = Tile(x,y,'Bridge/L.png')
                        tile.rect.height -= 1*coeff
                        self.tiles.add(tile)
                        self.semi_collide_tiles.add(tile)

                    elif level_data[i][j+1] == 0 and (level_data[i][j-1] == 2 or level_data[i][j-1] == 1) and (level_data[i-1][j] == 0 or level_data[i-1][j] == 5 or level_data[i-1][j] == 4) and level_data[i+1][j] == 0:
                        tile = Tile(x,y,'Bridge/R.png')
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

    def horizontal_movement_collision(self):
        for player in self.players_list:
            check_semi_collide, player.slide_allowed, player.detect_wall_collision = True, False, False
            player.rect.x += player.direction.x * player.speed

            for sprite in self.collide_tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    check_semi_collide = False
                    if player.direction.x < 0 or (player.push > 0 and player.opponent_flip) :
                        if player.wall_jump_left:
                            player.wall_collision = True
                            player.wall_jump_left, player.wall_jump_right = False, True
                        player.rect.left = sprite.rect.right
                        player.slide_allowed, player.detect_wall_collision = True, True
                    elif player.direction.x > 0 or (player.push > 0 and not player.opponent_flip):
                        if player.wall_jump_right:
                            player.wall_collision = True
                            player.wall_jump_left, player.wall_jump_right = True, False
                        player.rect.right = sprite.rect.left
                        player.slide_allowed, player.detect_wall_collision = True, True
            
            if check_semi_collide:
                for sprite in self.semi_collide_tiles.sprites():
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.x < 0 and not player.down_movement or (player.push > 0 and player.opponent_flip):
                            if player.wall_jump_left:
                                player.wall_collision = True
                                player.wall_jump_left, player.wall_jump_right = False, True
                            player.rect.left = sprite.rect.right
                        elif player.direction.x > 0 and not player.down_movement or (player.push > 0 and not player.opponent_flip):
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
        bonus_choice = random.choice(['speed','attack', 'attack_speed', 'health', 'resistance', 'spell', 'minotaur', 'demon', 'cyclop'])
        self.current_bonus = Bonus(bonus_choice)
        self.bonus_group.add(self.current_bonus)
    
    def bonus_collision(self, player):
        if player.rect.colliderect(self.current_bonus.rect):
            self.current_bonus.effect(player)
            self.bonus_group.remove(self.current_bonus)
            self.timer = 0 
            player.effect_ongoing = True
        
    def bonus_update(self):
        if not self.bonus_group:
            self.timer += 0.1
            if self.timer_check:
                self.timer_stop = random.randint(10,20)
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
            player1.damage( player2.attack*player2.attack_boost , player2.flip )
        if player2.rect.colliderect(player1.attack_rect) and not player2.temp_invincibility:
            player2.damage( player1.attack*player1.attack_boost , player1.flip )

    def run(self):
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
            player.update(self.display_surface)
            player.clear_effects()
        
        # bonus
        self.bonus_update()