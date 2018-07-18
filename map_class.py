from vector import Vector2


class Map():
	def __init__(self, size):
		# size 是 2 元 tuple
		self.size = Vector2(*size)
		self.block = []   # 任何东西都算是 block，带有功能性的也算

	def load_block(self, block):
		self.block = block