import pyray

class IntVec2:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

	def __add__(self, other):
		return IntVec2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return IntVec2(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar):
		return IntVec2(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return IntVec2(self.x * scalar, self.y * scalar)

	def __neg__(self, other):
		return IntVec2(-self.x, -self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def length(self):
		return pyray.vector2_length(self.to_pyray_vector2())

	def to_pyray_vector2(self):
		return pyray.Vector2(self.x, self.y)
