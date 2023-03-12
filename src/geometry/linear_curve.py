import pyray
from util import IntVec
from geometry.curve_helpers import BoundingBox, CurveIntersection

class LinearCurve:
	def __init__(self, p0, p2):
		self.p0 = IntVec(p0)
		self.p2 = IntVec(p2)

	# Currently yellow is used instead of the given color to highlight linear curves
	def draw(self, color, thickness=2): # pragma: no cover
		pyray.draw_line_ex(
			self.p0.to_pyray_vector2(),
			self.p2.to_pyray_vector2(),
			thickness, pyray.YELLOW
		)

	def draw_lines(self, color): # pragma: no cover
		pass

	def eval(self, t):
		return self.p0 + t * (self.p2 - self.p0)

	def eval_x(self, t):
		return self.p0.x + t * (self.p2.x - self.p0.x)

	def eval_y(self, t):
		return self.p0.y + t * (self.p2.y - self.p0.y)

	def derivative(self, t):
		return self.p2 - self.p0

	def second_derivative(self):
		return IntVec(0, 0)

	def parity_of_vertical_line_intersections(self, line_x):
		if self.p0.x < self.p2.x:
			return int(self.p0.x <= line_x < self.p2.x)

		if self.p2.x < self.p0.x:
			return int(self.p2.x < line_x <= self.p0.x)

		return 0

	def find_vertical_line_intersections(self, line_x):
		if self.parity_of_vertical_line_intersections(line_x) == 0:
			return []

		return [(line_x - self.p0.x) / (self.p2.x - self.p0.x)]

	def find_parabolic_curve_intersections(self, other):
		if self.p0.x == self.p2.x:
			if self.p0.y == self.p2.y:
				return []

			line_x = self.p0.x
			curve = other

			start_y = self.p0.y
			end_y = self.p2.y
		else:
			a = self.p0.y - self.p2.y
			b = self.p2.x - self.p0.x

			p0 = IntVec(a * other.p0.x + b * other.p0.y, other.p0.x)
			p1 = IntVec(a * other.p1.x + b * other.p1.y, other.p1.x)
			p2 = IntVec(a * other.p2.x + b * other.p2.y, other.p2.x)

			line_x = self.p0.y * self.p2.x - self.p0.x * self.p2.y
			curve = type(other)(p0, p1, p2)

			start_y = self.p0.x
			end_y = self.p2.x

		roots = curve.find_vertical_line_intersections(line_x)
		results = []

		for root in roots:
			h = end_y - start_y
			y = curve.eval_y(root) - start_y

			if 0 <= y*h < h*h:
				results.append(CurveIntersection(other, self, root, y / h))

		return results

	def find_intersections(self, other):
		if isinstance(other, LinearCurve):
			intersection = find_line_intersection(self, other, clip=True)

			return [i for i in (intersection,) if i is not None]

		return self.find_parabolic_curve_intersections(other)

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

	def transformed(self, f):
		return LinearCurve(f(self.p0), f(self.p2))

	def change_endpoint(self, new_endpoint):
		return LinearCurve(self.p0, new_endpoint)

def find_line_intersection(line1, line2, clip, dir1=None, dir2=None):
	if dir1 is None: dir1 = line1.p2 - line1.p0
	if dir2 is None: dir2 = line2.p2 - line2.p0

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
