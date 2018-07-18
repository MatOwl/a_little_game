import pygame
from vector import Vector2

def acc(unit, time):
	if abs(unit.speed.x) < unit.speed_lim:
		unit.speed += Vector2(unit.acc_r * time * unit.change_speed[0], 0)   # 因为 change_speed[0] 已经判定过不是0
		if abs(unit.speed.x) > unit.speed_lim: 
			unit.speed = Vector2(unit.speed.x / abs(unit.speed.x) * unit.speed_lim, unit.speed.y)


def decc(unit, time):
	absolute = abs(unit.speed.x)
	if absolute > 0:
		unit.speed = Vector2(unit.speed.x * 0.9, unit.speed.y)
		if abs(unit.speed.x) < 10: 
			unit.speed = Vector2(0, unit.speed.y)
	else:
		unit.change_speed[1] = 0

def gravity(unit, time, g):
	if not unit.contact['bottom']:
		if unit.float_state and unit.speed.y > 0:
			unit.float_accelaration(g, time)
		else:
			unit.speed = Vector2(unit.speed.x, min(unit.speed.y + g * time, 2000))

def collide(target, block, return_rect):

	collide_list = {'top':0, 'bottom': 0,'left': 0, 'right':0}
	if return_rect:
		rect_list = {'top':None, 'bottom': None,'left': None, 'right': None}

	for i in target.keys():
		collide_rect =	target[i].collidelist(block)
		if collide_rect == -1:
			collide_list[i] = 0
		else:
			collide_list[i] = 1
			if return_rect:
				rect_list[i] = block[collide_rect]

	if return_rect:
		return (collide_list, rect_list)
	else:
		return collide_list