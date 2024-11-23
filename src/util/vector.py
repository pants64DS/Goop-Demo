import pyray
import math

def get_result_type(v, x):
	if isinstance(v, FloatVec) or isinstance(x, (float, FloatVec)):
		return FloatVec

	if isinstance(x, (int, IntVec)):
		return IntVec

	if all(isinstance(y, int) for y in x):
		return IntVec

	return FloatVec

class Vector:
	def __init__(self, *scalars):
		if len(scalars) == 1 and isinstance(scalars[0], (list, tuple, Vector)):
			scalars = scalars[0]

		self.scalars = [self.convert_scalar(scalar) for scalar in scalars]

	def __getitem__(self, key):
		return self.scalars.__getitem__(key)

	def __setitem__(self, key, value):
		return self.scalars.__setitem__(key, self.convert_scalar(value))

	def __len__(self):
		return len(self.scalars)

	@property
	def x(self):
		return self[0]

	@property
	def y(self):
		return self[1]

	@x.setter
	def x(self, value):
		self[0] = value

	@y.setter
	def y(self, value):
		self[1] = value

	def __add__(self, other):
		result = [a + b for a, b in zip(self, other)]

		return get_result_type(self, other)(*result)

	def __sub__(self, other):
		result = [a - b for a, b in zip(self, other)]

		return get_result_type(self, other)(*result)

	def __mul__(self, scalar):
		result = [a * scalar for a in self]

		return get_result_type(self, scalar)(*result)

	def __rmul__(self, scalar):
		result = [scalar * a for a in self]

		return get_result_type(self, scalar)(*result)

	def __floordiv__(self, scalar):
		result = [a // scalar for a in self]

		return get_result_type(self, scalar)(*result)

	def __truediv__(self, scalar):
		result = [a / scalar for a in self]

		return FloatVec(*result)

	def __neg__(self):
		return type(self)(*[-a for a in self])

	def __eq__(self, other):
		return len(self) == len(other) and all(a == b for a, b in zip(self, other))

	def __str__(self):
		return f"({', '.join([str(x) for x in self])})"

	def __repr__(self):
		return type(self).__name__ + str(self)

	def __hash__(self):
		return hash(tuple(self.scalars))

	def length(self):
		return math.hypot(*self)

	def dist(self, other):
		return (self - other).length()

	def to_pyray_vector2(self):
		return pyray.Vector2(int(self.x), int(self.y))

	@classmethod
	def from_pyray_vector2(cls, vector2):
		return cls(vector2.x, vector2.y)

class IntVec(Vector):
	def convert_scalar(self, scalar):
		return int(scalar)

class FloatVec(Vector):
	def convert_scalar(self, scalar):
		return float(scalar)

def get_angle_between(u, v):
	return math.atan2(u.x*v.y - v.x*u.y, u.x*v.x + u.y*v.y)
