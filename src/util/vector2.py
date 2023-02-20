import pyray
from math import atan2

class IntVec2:
	def __init__(self, *args):
		if len(args) == 1:
			args = args[0]

		self.scalars = [int(arg) for arg in args]

	@property
	def x(self):
		return self.scalars[0]

	@property
	def y(self):
		return self.scalars[1]

	@x.setter
	def x(self, value):
		self.scalars[0] = value

	@y.setter
	def y(self, value):
		self.scalars[1] = value

	def __getitem__(self, key):
		return self.scalars.__getitem__(key)

	def __add__(self, other):
		return IntVec2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return IntVec2(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar):
		return IntVec2(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return IntVec2(self.x * scalar, self.y * scalar)

	def __floordiv__(self, scalar):
		return IntVec2(self.x // scalar, self.y // scalar)

	def __neg__(self):
		return IntVec2(-self.x, -self.y)

	def __eq__(self, other):
		return self.scalars == other.scalars

	def __repr__(self):
		return f'IntVec2({self.x}, {self.y})'

	def __str__(self):
		return f'({self.x}, {self.y})'

	def length(self):
		return pyray.vector2_length(self.to_pyray_vector2())

	def dist(self, other):
		return (self - other).length()

	def to_pyray_vector2(self):
		return pyray.Vector2(self.x, self.y)

	@classmethod
	def from_pyray_vector2(cls, vector2):
		return cls(vector2.x, vector2.y)

def get_angle_between(u, v):
	return atan2(u.x*v.y - v.x*u.y, u.x*v.x + u.y*v.y)
