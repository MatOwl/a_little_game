from vector import Vector2
import physics

import pygame
from pygame.locals import *
from sys import exit

from unit_class import *
from map_class import *

#----------------备忘---------------------
# This is only a reminder for me about what to add on or what to correct.
'''
关于碰撞的两个问题：
- 撞入墙里
- 穿墙
应对方案：当要进行快速移动时，先判定那个方向上多远有障碍物，
这个也可以顺便做成激光武器。

另外要设计好如何避免掉出世界之外。
'''
#--------------------------------------

pygame.init()   # initialise

#---------- Important parameters -----------
g = 1000
#------------------------------

#---------- Font -----------
font = pygame.font.SysFont("arial", 16)
font_height = font.get_linesize()
#-------------------------------

#----------- initialise background ----------
resol = (1280,720)
screen = pygame.display.set_mode(resol, 0 ,32)
background = pygame.Surface(resol)
background.fill((0,0,0))
#------------------------------

#----------- initialise clock --------
clock = pygame.time.Clock()
time_passed = 0
#------------------------------

#----------- initialise the main unit ----------   for now, there is only on controllable unit.
hero_size = (15,15)
hero = Pc(hero_size)
#-------------------------------

#----------- Load map --------------
my_map = Map(resol)
block = []
block_file = open('map.txt', 'r')

for i in block_file.readlines():
	if i: block.append(pygame.Rect(*eval(i)))

my_map.load_block(block)
#------------------------------------

#--------- load unit ------------------
all_unit = [hero]
#------------------------------------


#----------- Initialise the player-control unit ------------
hero.reset_pos(my_map)
#------------------------------

#---------- Initialise anything left ------------------
flag = True
#-----------------------------------------

# The main loop：
while True:

	# Retrive any important information
	pressed_keys = pygame.key.get_pressed()
	time_passed = clock.tick(60) / 1000.0
	mouse_pos = Vector2(*pygame.mouse.get_pos())

	# Retrive events/input
	for event in pygame.event.get():
		# event: closing
		if event.type == QUIT:
			exit()

		# event: single press
		if event.type == KEYDOWN:
			
			# face turning
			hero.face_turning(event.key == 97, event.key == 100)

			# event: space button  (key = 32)
			if event.key == 32:
				hero.space_movement(pressed_keys[K_s])

#			if event.key == 32 and event.mod == 1:   # previous setting
			if event.key == 107:
				hero.rush() 

			if event.unicode == 'r':
				hero.reset_pos(my_map)
				hero.set_spd((0,0))
				all_unit = [hero]

			if event.unicode == 'j':
				all_unit.append(hero.fire_normal())

		if event.type == MOUSEBUTTONDOWN:

			if event.button == 1:
				all_unit.append(hero.fire_normal())

			if event.button == 3:
				hero.rush()


	# Event: Holding button
	hero.float(pressed_keys[K_LSHIFT])
	hero.movement(pressed_keys[K_a], pressed_keys[K_d])
	
	# Event change in mouse pos
	facing = (mouse_pos - (hero.pos + hero.size * 0.5)).normalize()
	hero.set_facing(facing)

	# Update, unit:
	for i in all_unit:
		if not i.update_all(my_map, time_passed):
			all_unit.remove(i)

	# Update, physics
	physics.gravity(hero, time_passed, g)

	# blit
	screen.blit(background, (0,0))

	for i in my_map.block:
		temp = pygame.Surface(i.size)
		temp.fill((0,200,0))
		screen.blit(temp, i.topleft)

	hero_image = pygame.Surface(hero.size.value())
	hero_image.fill(hero.color)
	hero.set_image(hero_image)

	for i in all_unit:
		screen.blit(i.image, i.pos.value())

	screen.blit( font.render("hit_wall: " + str(hero.contact), True, (0, 0, 0)), (600, 650) )
	screen.blit( font.render("speed: " + str(hero.speed), True, (0, 0, 0)), (600, 670) )
	screen.blit( font.render("pos: " + str(hero.pos), True, (0, 0, 0)), (600, 680) )
	screen.blit( font.render("color: " + str(hero.color), True, (0, 0, 0)), (600, 660) )
	screen.blit( font.render("Units: " + str(all_unit), True, (0, 0, 0)), (600, 690) )


	pygame.display.update()

