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

	@property
	def x(self):
		return self.scalars[0]

	@property
	def y(self):
		return self.scalars[1]

	@x.setter
	def x(self, value):
		self.scalars[0] = self.convert_scalar(value)

	@y.setter
	def y(self, value):
		self.scalars[1] = self.convert_scalar(value)

	def __getitem__(self, key):
		return self.scalars.__getitem__(key)

	def __setitem__(self, key, value):
		return self.scalars.__setitem__(self.convert_scalar(key))

	def __add__(self, other):
		result = [a + b for a, b in zip(self.scalars, other.scalars)]

		return get_result_type(self, other)(*result)

	def __sub__(self, other):
		result = [a - b for a, b in zip(self.scalars, other.scalars)]

		return get_result_type(self, other)(*result)

	def __mul__(self, scalar):
		result = [a * scalar for a in self.scalars]

		return get_result_type(self, scalar)(*result)

	def __rmul__(self, scalar):
		result = [scalar * a for a in self.scalars]

		return get_result_type(self, scalar)(*result)

	def __floordiv__(self, scalar):
		result = [a // scalar for a in self.scalars]

		return get_result_type(self, scalar)(*result)

	def __truediv__(self, scalar):
		result = [a / scalar for a in self.scalars]

		return FloatVec(self, scalar)(*result)

	def __neg__(self):
		return type(self)(*[-a for a in self.scalars])

	def __eq__(self, other):
		return all(a == b for a, b in zip(self.scalars, other.scalars))

	def __str__(self):
		return f"({', '.join([str(x) for x in self.scalars])})"

	def length(self):
		return math.hypot(*self.scalars)

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

	def __repr__(self):
		return f"IntVec{self}"

class FloatVec(Vector):
	def convert_scalar(self, scalar):
		return float(scalar)

	def __repr__(self):
		return f"IntVec{self}"

def get_angle_between(u, v):
	return math.atan2(u.x*v.y - v.x*u.y, u.x*v.x + u.y*v.y)
