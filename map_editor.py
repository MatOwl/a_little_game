from vector import Vector2

import pygame
from pygame.locals import *
from sys import exit

class wall():

	def __init__(self, pivot):
		self.pivot = Vector2(*pivot)
		self.pos = Vector2(0,0)
		self.size = Vector2(0,0)

	def __str__(self):
		return "(%d, %d, %d, %d)" % (self.pos.x, self.pos.y, self.size.x, self.size.y)

	def settle(self, pos):
		self.size = Vector2(*pos) - self.pivot
		self.pos = Vector2(min(self.pivot.x, pos[0]), min(self.pivot.y, pos[1]))
		self.size = Vector2(abs(int(self.size.x)), abs(int(self.size.y)))

pygame.init()

resol = (1280,720)
screen = pygame.display.set_mode(resol, 0 ,32)
background = pygame.Surface((1280,720))
testing = pygame.Surface((1,1))
background.fill((0,0,0))

wall1 = wall((0,0))
wall2 = wall((0,600))
wall1.settle((1280, 10))
wall2.settle((1280,720))

my_map = [wall1,wall2]
trash_bin = []
state = 'free state'
pre_select = False

font = pygame.font.SysFont("arial", 16)
font_height = font.get_linesize()

while True:
	mouse_pos = pygame.mouse.get_pos()
	
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

		if event.type == MOUSEBUTTONUP and event.button == 1 and state == 'selecting state':
			state = 'free state'
			my_map.append(blk)
			trash_bin = []
			pre_select = False

		if event.type == MOUSEBUTTONDOWN and event.button == 3 and state == 'selecting state':
			state = 'free state'
			pre_select = False

		if event.type == KEYDOWN:
			if event.unicode == 's':
				file = open('map_0.txt', 'w')
				for i in my_map:
					file.write(str(i) + '\n')

			if event.key == 122 and event.mod == 64:
				if len(my_map) > 2:
					trash_bin.append(my_map.pop())
					if len(trash_bin) > 10:
						trash_bin = trash_bin[-10:]

			if event.key == 121 and event.mod == 64:
				try:
					my_map.append(trash_bin.pop())
				except IndexError:
					empty = True

			if event.unicode == 'd':
				flag = False
				for i in my_map[2:]:
					flag = flag or (0 < mouse_pos[0] - i.pos.x < i.size.x and 0 < mouse_pos[1] - i.pos.y < i.size.y)
					if flag:
						trash_bin.append(i)
						my_map.remove(i)
						break

	mouse_pressed = pygame.mouse.get_pressed()

	if mouse_pressed[0] and state == 'free state':
		state = 'selecting state'
		blk = wall(mouse_pos)

	if state == 'selecting state':
		# pos2 = pygame.mouse.get_pos()
		blk.settle(mouse_pos)
		if blk.size.x * blk.size.y > 25:
			pre_select = pygame.Surface((blk.size.x, blk.size.y))
			pre_select.fill((0,100,0))

	screen.blit(background, (0,0))
	
	for i in my_map:
		block = pygame.Surface((i.size.x, i.size.y))
		block.fill((0,200,0))
		screen.blit(block,(i.pos.x,i.pos.y))
	
	if pre_select:
		screen.blit(pre_select, (blk.pos.x, blk.pos.y))
		screen.blit( font.render("pivot: " + str(blk.pos), True, (255, 255, 255)), (20, 20) )

	screen.blit( font.render('pos: ' + str(mouse_pos), True, (255,255,255)), (20, 50))


	pygame.display.update()
