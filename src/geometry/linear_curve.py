import pyray
from geometry.curve_helpers import BoundingBox, CurveIntersection

class LinearCurve:
	def __init__(self, p0, p2):
		self.p0 = p0
		self.p2 = p2

	def draw(self, color, thickness=2):
		pyray.draw_line_ex(
			self.p0.to_pyray_vector2(),
			self.p2.to_pyray_vector2(),
			thickness, color
		)

	def draw_lines(self, color):
		pass

	def eval(self, t):
		return self.p0 + t * (self.p2 - self.p0)

	def eval_x(self, t):
		return self.p0.x + t * (self.p2.x - self.p0.x)

	def eval_y(self, t):
		return self.p0.y + t * (self.p2.y - self.p0.y)

	def derivative(self, t):
		return self.p2 - self.p0

	def parity_of_vertical_line_intersections(self, line_x):
		if self.p0.x < self.p2.x:
			return int(self.p0.x <= line_x < self.p2.x)

		if self.p2.x < self.p0.x:
			return int(self.p2.x < line_x <= self.p0.x)

		return 0

	def find_vertical_line_intersections(self, line_x):
		if self.parity_of_vertical_line_intersections(line_x) == 0:
			return []

		return [self.eval_y((line_x - self.p0.x) / (self.p2.x - self.p0.x))]

	def find_parabolic_curve_intersections(self, other):
		raise NotImplementedError("An intersection between a parabola and a line")

	def find_intersections(self, other):
		if isinstance(other, LinearCurve):
			intersection = find_line_intersection(self, other, clip=True)

			if intersection is None:
				return []

			return intersection

		return self.find_parabolic_curve_intersections(self)

	def starts_going_left(self):
		return self.p0.x > self.p2.x

	def ends_going_left(self):
		return self.p0.x > self.p2.x

	def get_side_vectors(self):
		return [self.p2 - self.p0]

	def get_bounding_box(self):
		return BoundingBox(self.p0, self.p2)

	def clip_until(self, t):
		return LinearCurve(self.eval(t), self.p2)

	def clip_after(self, t):
		return LinearCurve(self.p0, self.eval(t))

	def clip_after_until(self, t1, t2):
		return LinearCurve(self.eval(t1), self.eval(t2))

def find_line_intersection(line1, line2, clip):
	dir1 = line1.p2 - line1.p0
	dir2 = line2.p2 - line2.p0

	det = dir1.x * dir2.y - dir2.x * dir1.y

	if det == 0:
		return None

	offset = line2.p0 - line1.p0

	t1 = dir2.y * offset.x - dir2.x * offset.y
	t2 = dir1.y * offset.x - dir1.x * offset.y

	if clip:
		if t1 * det < 0 \
		or t2 * det < 0 \
		or t1 * det >= det * det \
		or t2 * det >= det * det:
			return None

	return CurveIntersection(line1, line2, t1 / det, t2 / det)
