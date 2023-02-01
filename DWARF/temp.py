import pygame, sys
from random import randint
from functions import *
from copy import deepcopy
from math import *
from Heroes_Dico import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos, choice, group):
		super().__init__(group)
		self.direction = pygame.math.Vector2()
		self.speed = 4
		if choice == 1:
			self.image = all_animations[1][0][0]
			self.rect = self.image.get_rect(topleft = pos)
			self.move_keys = {'up': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'sprint': pygame.K_LSHIFT}
		else:
			self.image = all_animations[3][0][0]
			self.rect = self.image.get_rect(topleft = pos)
			self.move_keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'sprint': pygame.K_RCTRL}
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[self.move_keys['up']]:
			self.direction.y = -1
		elif keys[self.move_keys['down']]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[self.move_keys['right']]:
			self.direction.x = 1
		elif keys[self.move_keys['left']]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# ground
		self.ground_surf = pygame.image.load('DWARF/test_background.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		# zoom 
		self.zoom_scale = 1
		self.internal_surf_size = (1280,617)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(topleft = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self,target1, target2):
		self.offset.x = (target1.rect.centerx + target2.rect.centerx)/2 - self.half_w
		self.offset.y = (target1.rect.centery + target2.rect.centery)/2 - self.half_h

		# Add limits for camera movement
		#self.offset.x = max(0, min(self.offset.x, self.ground_surf.get_width() - self.display_surface.get_width()))
		#self.offset.y = max(0, min(self.offset.y, self.ground_surf.get_height() - self.display_surface.get_height()))

	def custom_draw(self,player1, player2):
		
		self.center_target_camera(player1, player2)
		self.internal_surf.fill('#71ddee')

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
		self.internal_surf.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image,offset_pos)

		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

		self.display_surface.blit(scaled_surf,scaled_rect)


pygame.init()
screen = pygame.display.set_mode((1280,617))
clock = pygame.time.Clock()
pygame.event.set_grab(True)

all_animations = store_animations([skeleton_dico_v1],[santa_dico_v2,minotaur_dico_v2,dwarf_dico_v2, indiana_jones_dico_v2, adventurer_dico_v2, bat_dico_v2, halo_dico_v2,gladiator_dico_v2, demon_dico_v2, cyclop_dico_v2],[hobbit_dico_v3])

# setup 
camera_group = CameraGroup()

player1 = Player((0,0),1,camera_group)
player2 = Player((1280,617),2,camera_group)
player_group = pygame.sprite.Group()
player_group.add(player1,player2)

player1_pos_save, player2_pos_save = deepcopy([player1.rect.x, player1.rect.y]), deepcopy([player2.rect.x, player2.rect.y])
difference_save = [abs(player1.rect.x-player2.rect.x),abs(player1.rect.y-player2.rect.y)]
difference_length_save = sqrt(difference_save[0]*difference_save[0]+difference_save[1]*difference_save[1])

for i in range(20):
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_k:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEWHEEL:
			camera_group.zoom_scale += event.y * 0.03
	difference = [abs(player1.rect.x-player2.rect.x),abs(player1.rect.y-player2.rect.y)]
	difference_length = sqrt(difference[0]*difference[0]+difference[1]*difference[1]) # pythagore
	new_length = abs(difference_length - difference_length_save)

	if 900 > difference_length > 800:
		if difference_length < difference_length_save:
			camera_group.zoom_scale += 0.001*new_length

		elif difference_length > difference_length_save:
			camera_group.zoom_scale += -0.001*new_length

	elif 600 > difference_length > 500:
		if difference_length < difference_length_save:
			camera_group.zoom_scale += 0.002*new_length

		elif difference_length > difference_length_save:
			camera_group.zoom_scale += -0.002*new_length

	elif 400 > difference_length > 300:
		if difference_length < difference_length_save:
			camera_group.zoom_scale += 0.008*new_length

		elif difference_length > difference_length_save:
			camera_group.zoom_scale += -0.008*new_length

	print(difference_length)
	screen.fill('#71ddee')
	camera_group.update()
	camera_group.custom_draw(player1, player2)
	player1_pos_save, player2_pos_save = deepcopy([player1.rect.x,player1.rect.y]), deepcopy([player2.rect.x,player2.rect.y])
	difference_length_save = deepcopy(difference_length)
	pygame.display.update()
	clock.tick(60)
	