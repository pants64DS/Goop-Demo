from math import sqrt
import numpy
import pyray
from util.vector2 import IntVec2

# Returns true when (-b - sqrt(bb - 4ac)) / (2a) >= 0
def is_first_root_nonnegative(a, b, c):
	if a > 0:
		return b <= 0 <= c
	else:
		return b >= 0 or c >= 0

# Returns true when (-b + sqrt(bb - 4ac)) / (2a) >= 0
def is_second_root_nonnegative(a, b, c):
	if a > 0:
		return b <= 0 or c <= 0
	else:
		return c <= 0 <= b

# Returns true when (-b - sqrt(bb - 4ac)) / (2a) < 1
def is_first_root_below_one(a, b, c):
	if a > 0:
		return a + b < -c or b > -2 * a
	else:
		return a + b < -c and b <= -2 * a

# Returns true when (-b + sqrt(bb - 4ac)) / (2a) < 1
def is_second_root_below_one(a, b, c):
	if a > 0:
		return a + b > -c and b >= -2 * a
	else:
		return a + b > -c or b < -2 * a

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec2(p0)
		self.p1 = IntVec2(p1)
		self.p2 = IntVec2(p2)

	def get_coeff_vectors(self):
		return self.p0, \
			2 * (self.p1 - self.p0), \
			self.p0 + self.p2 - 2 * self.p1

	def get_x_coeffs(self):
		return self.p0.x, \
			2 * (self.p1.x - self.p0.x), \
			self.p0.x + self.p2.x - 2 * self.p1.x

	def get_y_coeffs(self):
		return self.p0.y, \
			2 * (self.p1.y - self.p0.y), \
			self.p0.y + self.p2.y - 2 * self.p1.y

	def eval(self, t):
		coeffs = self.get_coeff_vectors()

		return coeffs[0] + (coeffs[1] + coeffs[2] * t) * t

	def eval_x(self, t):
		coeffs = self.get_x_coeffs()

		return coeffs[0] + (coeffs[1] + coeffs[2] * t) * t

	def eval_y(self, t):
		coeffs = self.get_y_coeffs()

		return coeffs[0] + (coeffs[1] + coeffs[2] * t) * t

	def derivative(self, t):
		coeffs = self.get_coeff_vectors()

		return coeffs[1] + 2 * coeffs[2] * t

	def parity_of_vertical_line_intersections(self, line_x):
		# The edge cases here are the most complicated
		if line_x == self.p0.x:
			if self.p0.x == self.p2.x:
				return 1
			elif self.p0.x < self.p2.x:
				return int(self.p1.x >= line_x)
			else:
				return int(self.p1.x <= line_x)

		if line_x == self.p2.x:
			if self.p0.x < self.p2.x:
				return int(self.p1.x > line_x)
			else:
				return int(self.p1.x < line_x)

		lo, hi = sorted((self.p0.x, self.p2.x))

		return int(lo < line_x < hi)

	def draw(self, color, thickness=2):
		pyray.draw_line_bezier_quad(
			self.p0.to_pyray_vector2(),
			self.p2.to_pyray_vector2(),
			self.p1.to_pyray_vector2(),
			thickness, color
		)

	def draw_lines(self, color):
		pyray.draw_line(self.p0.x, self.p0.y, self.p1.x, self.p1.y, color)
		pyray.draw_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, color)

	def find_vertical_line_intersections(self, line_x):
		a = self.p0.x + self.p2.x - 2 * self.p1.x
		b = 2*(self.p1.x - self.p0.x)
		c = self.p0.x - line_x

		if a == 0:
			if b*c <= 0 and -b*c < b*b:
				return [self.eval_y(-c / b)]
			else:
				return []

		discriminant = b*b - 4*a*c

		if discriminant <= 0:
			return []

		results = []

		if is_first_root_nonnegative(a, b, c) and is_first_root_below_one(a, b, c):
			root = (-b - sqrt(b*b - 4*a*c)) / (2*a)
			results.append(self.eval_y(root))

		if is_second_root_nonnegative(a, b, c) and is_second_root_below_one(a, b, c):
			root = (-b + sqrt(b*b - 4*a*c)) / (2*a)
			results.append(self.eval_y(root))

		return results

	def find_intersections(self, other):
		# Construct a matrix for a linear map that makes the parabolas perpendicular
		m1 =   self.p0.y +  self.p2.y - 2 *  self.p1.y
		m2 = -other.p0.y - other.p2.y + 2 * other.p1.y
		m3 =  -self.p0.x -  self.p2.x + 2 *  self.p1.x
		m4 =  other.p0.x + other.p2.x - 2 * other.p1.x

		det = m1 * m4 - m3 * m3
		if det == 0:
			raise NotImplementedError("Parabolas with parallel axes")

		# Apply the linear map to the control points
		p0x = self.p0.x * m1 + self.p0.y * m3
		p0y = self.p0.x * m2 + self.p0.y * m4
		p1y = self.p1.x * m2 + self.p1.y * m4
		p2x = self.p2.x * m1 + self.p2.y * m3
		p2y = self.p2.x * m2 + self.p2.y * m4

		q0x = other.p0.x * m1 + other.p0.y * m3
		q0y = other.p0.x * m2 + other.p0.y * m4
		q1x = other.p1.x * m1 + other.p1.y * m3
		q2x = other.p2.x * m1 + other.p2.y * m3
		q2y = other.p2.x * m2 + other.p2.y * m4

		# Combine the equations of the curves
		a1 = p0y + p2y - 2 * p1y
		b1 = 2 * (p1y - p0y)
		c1 = p0y - q0y

		h = q2y - q0y
		a2 = q0x + q2x - 2 * q1x
		b2 = 2 * (q1x - q0x)
		c2 = q0x - p0x

		int_coeffs = [
			c1*(h*b2 + c1*a2) + h*h*c2,
			h*b1*b2 + 2*b1*c1*a2 + h*h*(p0x - p2x),
			h*a1*b2 + (2*a1*c1 + b1*b1)*a2,
			2*a1*b1*a2,
			a1*a1*a2
		]

		max_coeff = max(int_coeffs, key=abs)
		f = numpy.polynomial.Polynomial([coeff / max_coeff for coeff in int_coeffs])

		# Solve for the intersections and discard any of them that lie outside of either curve
		results = []
		lo, hi = sorted((q0y, q2y))

		for root in f.roots():
			t1 = numpy.real(root)
			if abs(numpy.imag(root)) < 1e-5 and 0 <= t1 < 1:
				t2 = (a1*t1 + b1) * t1 + p0y
				if lo <= t2 < hi:
					results.append(CurveIntersection(self, other, t1, (t2 - q0y) / (q2y - q0y)))

		return results

	def clip_until(self, t):
		p0 = self.eval(t)
		p1 = line_intersection(Line(p0, self.derivative(t)), Line(self.p2, self.p1 - self.p2))

		return Curve(p0, p1, self.p2)

	def clip_after(self, t):
		p2 = self.eval(t)
		p1 = line_intersection(Line(p2, self.derivative(t)), Line(self.p0, self.p1 - self.p0))

		return Curve(self.p0, p1, p2)

	def clip_after_until(self, t1, t2):
		p0 = self.eval(t1)
		p2 = self.eval(t2)
		p1 = line_intersection(Line(p0, self.derivative(t1)), Line(p2, self.derivative(t2)))

		return Curve(p0, p1, p2)

class Line:
	def __init__(self, pos, dir):
		self.pos = pos
		self.dir = dir

def line_intersection(l1, l2):
	t = (l2.dir.x * (l1.pos.y - l2.pos.y) + l2.dir.y * (l2.pos.x - l1.pos.x)) / (l1.dir.x * l2.dir.y - l2.dir.x * l1.dir.y)

	return l1.pos + l1.dir * t


class CurveIntersection:
	def __init__(self, curve1, curve2, t1, t2):
		self.curve1 = curve1
		self.curve2 = curve2
		self.t1 = t1
		self.t2 = t2

	def get_pos(self):
		# return self.curve1.eval(self.t1)
		return self.curve2.eval(self.t2)

	def get_pos_x(self):
		# return self.curve1.eval_x(self.t1)
		return self.curve2.eval_x(self.t2)

	def get_pos_y(self):
		# return self.curve1.eval_y(self.t1)
		return self.curve2.eval_y(self.t2)

