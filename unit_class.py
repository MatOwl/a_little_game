from vector import Vector2
from pygame.locals import *
import physics
import pygame

class Unit():

	def __init__(self, size):
		# 外观 和 碰撞判定
		self.size = Vector2(*size)
		self.image = None
		self.color = (255,255,255)

		# 位置 和 碰撞判定
		self.pos = Vector2(0,0)
		self.update_sides()
		self.facing = Vector2(1,0)   # 两个参数，是单位圆上的点的坐标

		# 位移相关数据
		self.speed = Vector2(0,0)   # 当前速度
		self.speed_lim = 400   # 总最高速度（注意是用勾股定理计算）
		self.acc_r = 3000   # 平移加速度
		self.change_speed = [0,0]

		# 碰撞情况记录 和 空中状况
		self.contact = {'top':1, 'bottom': 1,'left': 1, 'right':1}


	# 位置检定：
	def update_sides(self):		
		top = pygame.Rect( (self.pos + Vector2(0,-1)).value(), (self.size.x, 1) )
		bottom = pygame.Rect( (self.pos + Vector2(0 ,self.size.y)).value(), (self.size.x, 1) )
		left = pygame.Rect( (self.pos + Vector2(-1,0)).value(), (1, self.size.y) )
		right = pygame.Rect( (self.pos + Vector2(self.size.x, 0)).value(), (1,self.size.y) )
		self.sides = {'top':top, 'bottom': bottom,'left': left, 'right':right}

	def update_side_checkers(self):	
		length = 30
		top = pygame.Rect( (self.pos + Vector2(0,-length)).value(), (self.size.x, length) )
		bottom = pygame.Rect( (self.pos + Vector2(0 ,self.size.y)).value(), (self.size.x, length) )
		left = pygame.Rect( (self.pos + Vector2(-length,0)).value(), (length, self.size.y) )
		right = pygame.Rect( (self.pos + Vector2(self.size.x, 0)).value(), (length,self.size.y) )
		return {'top':top, 'bottom': bottom,'left': left, 'right':right}

	def update_collision(self, block):
		# 其中，block 是个 rect list，是 Map 对象的一个参数。
		self.contact = physics.collide(self.sides, block, False)


	def update_according_collision(self):   # 速度修正
		
		if self.contact['top'] and self.speed.y < 0: 
			self.speed = Vector2(self.speed.x,0)

		if self.contact['bottom'] and self.speed.y > 0: 
			self.speed = Vector2(self.speed.x,0)
		
		if self.contact['left'] and self.speed.x < 0: 
			self.speed = Vector2(0,self.speed.y)
		
		if self.contact['right'] and self.speed.x > 0: 
			self.speed = Vector2(0,self.speed.y)

	# 重置 与 参数修改：

		

	def set_pos(self, pos):
		# pos 是 2 元 tuple
		self.pos = Vector2(*pos)

	def set_spd(self, speed):
		# speed 是 2 元 tuple
		self.speed = Vector2(*speed)

	def set_size(self, size):
		# size 是 2 元 tuple
		self.size = Vector2(*size)

	def set_image(self, image):
		self.image = image

	def reset_color(self):
		self.color = (255,255,255)

	def set_color(self, color):
		# color 是一个 3 元 tuple，RGB 颜色
		self.color = color

	

	# 运动
	def motion(self, time, block):
		# self.update_according_collision()
		checker = self.update_side_checkers()

		self.pos = self.speed * time + self.pos

		rect = pygame.Rect(self.pos.value(), self.size.value())
		collision = rect.collidelist(block)

		if collision != -1:
			result = physics.collide(checker, block, True)
			# print(str(result) + '\n' + str(self.pos))
			if result[0]['top']:
				self.pos = Vector2(self.pos.x, result[1]['top'].bottom)
				self.speed.y = 0
			elif result[0]['bottom']:
				self.pos = Vector2(self.pos.x, result[1]['bottom'].top - self.size.y)
				self.speed.y = 0

			if result[0]['left']:
				self.pos = Vector2(result[1]['left'].right, self.pos.y)
				self.speed.x = 0
			elif result[0]['right']:
				self.pos = Vector2(result[1]['right'].left - self.size.x, self.pos.y)
				self.speed.x = 0


		self.update_sides()


	def face_turning(self, l_key, r_key):
		# l_key/r_key 就是是否往左/右走。
		if l_key and self.facing.x >= 0:
			self.facing = Vector2(-self.facing.x, self.facing.y)
		if r_key and self.facing.x <= 0:
			self.facing = Vector2(-self.facing.x, self.facing.y)



	def acceleration(self, time_passed):   # 结算一般运动时速度变化。
		if self.change_speed[0]:
			physics.acc(self, time_passed)
		if self.change_speed[1]:
			physics.decc(self, time_passed)

		if self.speed.x == 0:
			self.change_speed[1] = 0


class Pc(Unit):

	def __init__(self, size):
		Unit.__init__(self, size)

		self.rush_state = 0  # rush 一次就减一，落地或者碰墙就回归到3
		self.rush_time = 3   # unit sec
		self.jump_state = 1
		self.drop_state = 1
		self.drop_time = False   # bool
		self.float_state = False

	def update_all(self, my_map, time_passed):
		self.update_collision(my_map.block)
		self.update_according_pos()
		self.update_jump()

		if self.rush_time: 	# to check whether any special action in the air is on
			self.update_rush(time_passed)
		else:
			self.acceleration(time_passed)

		self.motion(time_passed, my_map.block)

		return True


	def update_rush(self, time_passed):
		self.rush_time -= time_passed
		if self.rush_time < 0: 
			self.rush_end()

	def update_jump(self):
		if self.speed.y > 0 and not self.rush_time and not self.drop_time:   # 过了最高点 而且 没有在 rush， 而且 drop 还没用
			self.jump_end()   # 颜色回归正常

	# 位置相关修正
	def update_according_pos(self):   # 动作刷新
		if self.contact['bottom']:
			self.reset_action_ground()
		else:
			self.reset_action_air()

	def reset_pos(self, my_map):
		# self.pos = Vector2(300,300)
		
		pos = (my_map.size - self.size) * 0.5
		pos = pos.value()

		resol = my_map.size.value()

		self.set_pos(pos)

		
		rect = pygame.Rect(self.pos.value(), self.size.value())
		collision = rect.collidelist(my_map.block)
		
		while collision != -1:   # 如果还碰撞，那就旋转并延长一丢丢
			pos = [pos[0] - resol[0]/2, - (pos[1] - resol[1]/2)]
			pos = [ (pos[0] * 0.96592583 + pos[1]*(-0.25881905)) * 1.1, (pos[0]*(0.25881905) + pos[1]* (0.96592583)) * 1.1]
			pos = [pos[0] + resol[0]/2, - pos[1] + resol[1]/2]
			self.set_pos(pos)
			rect = pygame.Rect(self.pos.value(), self.size.value())
			collision = rect.collidelist(my_map.block)

	def reset_action_ground(self):   # rush and jump,落地刷新
		self.rush_state = 3
		self.jump_state = 10
		if self.drop_time: self.drop_end()   # drop_state == 0 就是下落中。

	def reset_action_air(self):   # drop，空中更新
		self.drop_state = 1

	def movement(self, l_key, r_key):   # 按键到修改状态改变
		if self.change_speed[0] == 0:
			if l_key:
				self.change_speed[0] = -1
			if r_key:
				self.change_speed[0] = 1
		else:
			if not l_key and self.change_speed[0] == -1:
				self.change_speed[0] = 0
				self.change_speed[1] = -1
			if not r_key and self.change_speed[0] == 1:
				self.change_speed[0] = 0
				self.change_speed[1] = 1

	def space_movement(self, key):
		# key 就是布尔型，是否按下 s
		if key:
			self.drop()   # 下坠
		else:
			self.jump()   # 跳


	# 空中动作
	def jump(self):
		if self.jump_state:
			self.speed += Vector2(0, -600)
			self.set_color((0,0,255))  # 跳跃时的外观改变
			self.jump_state -= 1

	def jump_end(self):
		self.reset_color()

	def drop(self):
		if self. drop_state:
			self.speed = Vector2(0, 1500)
			self.set_color((0,0,100))
			self.drop_time = True
			self.drop_state = 0

	def drop_end(self):
		self.reset_color()   # 也可以加一个动画
		self.drop_time = False

	def rush(self):
		if self.rush_time == 0 and self.rush_state:
			if self.facing.x > 0:
				direction = 1
			elif self.facing.x < 0:
				direction = -1
			else:
				direction = 0
			self.speed = Vector2( direction * 1500, 0 )
			self.set_color((255,0,0))   # rush 的时候外观改变
			self.rush_time = 0.1
			self.rush_state -= 1

	def rush_end(self):
		self.rush_time = 0
		self.set_spd((0,0))
		self.reset_color()

	def float(self, key):
		if key:
			self.float_state = True
		else:
			self.float_state = False

	def float_accelaration(self, g, time):
		self.speed = Vector2(self.speed.x, min(self.speed.y + g * time * 0.05, 70))

	# fire!!
	def fire_normal(self):
		# initialise a bullet

		bullet_size = (3,3)

		bullet_image = pygame.Surface(bullet_size)
		bullet_image.fill((255,255,255))
		
		bullet_details = {
		'range': 400,
		'lifetime': 4, 
		'image': bullet_image,
		'speed': 1000
		}
		return Bullet(bullet_size, self.facing.value(), (self.pos + self.size * 0.5).value(), bullet_details)



class Bullet(Unit):

	def __init__(self, size, facing, pos, details):
		# details = {range: , lifetime: , image: }

		Unit.__init__(self, size)

		self.set_pos(pos)
		self.set_image(details['image'])

		self.facing = Vector2(*facing)   # facing is a 2d tuple
		self.init_pos = self.pos
		self.range = details['range']
		self.lifetime = details['lifetime']
		self.speed = self.facing.normalize() * details['speed']
		self.damage = 1   # 先不用

	def update_all(self, my_map, time_passed):
		self.motion(time_passed, my_map.block)
		
		return self.update_continue(my_map, time_passed) # True: continue to exist，False，delete


	def update_continue(self, my_map, time_passed):   
	# 检查 4 样：碰撞次数、与目标碰撞、range 和 生存时间
		self.update_collision(my_map.block)
		contact = False
		for i in self.contact.keys():
			contact = self.contact[i] or contact

		self.lifetime -= time_passed

		flag = contact or self.lifetime <= 0 or self.range <= (self.pos - self.init_pos).get_magnitude()

		return not flag