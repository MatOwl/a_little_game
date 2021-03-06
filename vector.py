import math

class Vector2(object):
	def __init__(self, x=0.0, y=0.0):
		if type(x) == tuple:
			self.x = x[0]
			self.y = x[1]
		elif type(x) == Vector2:
			self.x = x.x
			self.y = x.y
		else:
			self.x = x
			self.y = y
	
	def __str__(self):
		return "(%s, %s)"%(self.x, self.y)
	
	def value(self):
		return (self.x, self.y) 

	def value_int(self):
		return (int(self.x), int(self.y))

	@staticmethod
	def from_points(P1, P2):
		return Vector2( P2[0] - P1[0], P2[1] - P1[1] )
	
	def get_magnitude(self):
		return math.sqrt( self.x**2 + self.y**2 )
	
	def normalize(self):
		magnitude = self.get_magnitude()
		x = self.x / magnitude
		y = self.y / magnitude
		return Vector2(x,y)
	# rhs stands for Right Hand Side
	def __add__(self, rhs):
		return Vector2(self.x + rhs.x, self.y + rhs.y)

	def __sub__(self, rhs):
		return Vector2(self.x - rhs.x, self.y - rhs.y)

	def __neg__(self):
		return Vector2(-self.x, -self.y)

	def __mul__(self, scalar):
		return Vector2(self.x * scalar, self.y * scalar)
	
	def __turediv__(self, scalar):
		return Vector2(self.x / scalar, self.y / scalar)