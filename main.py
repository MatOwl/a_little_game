from vector import Vector2
import physics

import pygame
from pygame.locals import *
from sys import exit

from unit_class import *
from map_class import *

#----------------备忘---------------------
'''
关于碰撞的两个问题：
- 撞入墙里
- 穿墙
应对方案：当要进行快速移动时，先判定那个方向上多远有障碍物，
这个也可以顺便做成激光武器。

另外要设计好如何避免掉出世界之外。
'''
#--------------------------------------

pygame.init()   # 初始化

#---------- 全局参数 -----------
g = 1000
#------------------------------

#---------- 字体设置 -----------
font = pygame.font.SysFont("arial", 16)
font_height = font.get_linesize()
#-------------------------------

#----------- 背景设置 ----------
resol = (1280,720)
screen = pygame.display.set_mode(resol, 0 ,32)
background = pygame.Surface(resol)
background.fill((0,0,0))
#------------------------------

#----------- 时间初始化 --------
clock = pygame.time.Clock()
time_passed = 0
#------------------------------

#----------- 主角单位创建 ----------   单主角游戏
hero_size = (15,15)
hero = Pc(hero_size)
#-------------------------------

#----------- 地图加载 --------------
my_map = Map(resol)
block = []
block_file = open('map_0.txt', 'r')

for i in block_file.readlines():
	if i: block.append(pygame.Rect(*eval(i)))

my_map.load_block(block)
#------------------------------------

#----------- 单位初始化 ------------
hero.reset_pos(my_map)
#------------------------------

#---------- 其余数据初始化 ------------------
flag = True
#-----------------------------------------

# 循环部分：
while True:

	# 角色参数 update：
	hero.update_collision(my_map.block)
	hero.update_according_pos()

	# 获取各种相关数据
	pressed_keys = pygame.key.get_pressed()
	time_passed = clock.tick(60) / 1000.0

	# 获取 event 状况
	for event in pygame.event.get():
		# 关闭
		if event.type == QUIT:
			exit()

		# 单击按键情况
		if event.type == KEYDOWN:
			
			# 处理转向
			hero.face_turning(event.key == 97, event.key == 100)

			# 空格按键 event (key = 32)
			if event.key == 32:
				hero.space_movement(pressed_keys[K_s])

#			if event.key == 32 and event.mod == 1:
			if event.key == 107:
				hero.rush() 

			if event.unicode == 'r':
				hero.reset_pos(my_map)
				hero.set_spd((0,0))


	# 持续按键状态
	hero.float(pressed_keys[K_LSHIFT])

	# 角色运动状态改变
	hero.movement(pressed_keys[K_a], pressed_keys[K_d])
	
	hero.update_jump()
	physics.gravity(hero, time_passed, g)

	if hero.rush_time: 	# 空中动作是否完成判断，并计算速度变化
		hero.update_rush(time_passed)

	else:   # 普通运动状态，如果是冲刺，拉索，或其他特殊水平运动，请额外处理
		hero.acceleration(time_passed)
	
	# 位移结果 与 碰撞
	hero.update_collision(block)
	hero.motion(time_passed, my_map.block)

	# blit
	screen.blit(background, (0,0))
	for i in my_map.block:
		temp = pygame.Surface(i.size)
		temp.fill((0,200,0))
		screen.blit(temp, i.topleft)

	hero_image = pygame.Surface(hero.size.value())
	hero_image.fill(hero.color)
	hero.set_image(hero_image)
	screen.blit(hero.image, hero.pos.value())

	screen.blit( font.render("hit_wall: " + str(hero.contact), True, (0, 0, 0)), (600, 650) )
	screen.blit( font.render("speed: " + str(hero.speed), True, (0, 0, 0)), (600, 670) )
	screen.blit( font.render("pos: " + str(hero.pos), True, (0, 0, 0)), (600, 680) )
	screen.blit( font.render("color: " + str(hero.color), True, (0, 0, 0)), (600, 660) )


	pygame.display.update()

