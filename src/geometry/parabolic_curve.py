from math import sqrt
import numpy
import pyray
from geometry import LinearCurve, find_line_intersection, BoundingBox, CurveIntersection
from util import IntVec2

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

class ParabolicCurve:
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
			if self.p0.x < self.p2.x:
				return int(self.p1.x >= line_x)
			elif self.p2.x < self.p0.x:
				return int(self.p1.x <= line_x)
			else:
				return 1

		if line_x == self.p2.x:
			if self.p0.x < self.p2.x:
				return int(self.p1.x > line_x)
			else:
				return int(self.p1.x < line_x)

		lo, hi = sorted((self.p0.x, self.p2.x))

		return int(lo < line_x < hi)

	def get_bounding_box(self):
		return BoundingBox(self.p0, self.p1, self.p2)

	def draw(self, color, thickness=2):
		pyray.draw_line_bezier_quad(
			self.p0.to_pyray_vector2(),
			self.p2.to_pyray_vector2(),
			self.p1.to_pyray_vector2(),
			thickness, color
		)

	def draw_lines(self, color):
		color1 = pyray.GREEN if self.p0.x == self.p1.x else color
		color2 = pyray.GREEN if self.p2.x == self.p1.x else color

		pyray.draw_line(self.p0.x, self.p0.y, self.p1.x, self.p1.y, color1)
		pyray.draw_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, color2)

	def find_vertical_line_intersections(self, line_x):
		c, b, a = self.get_x_coeffs()
		c -= line_x

		if a == 0:
			if b*c <= 0 and -b*c < b*b:
				return [-c / b]
			else:
				return []

		discriminant = b*b - 4*a*c

		if discriminant < 0:
			return []

		if discriminant == 0:
			if c == 0:
				return [-b / (2*a)]
			else:
				return []

		results = []

		if is_first_root_nonnegative(a, b, c) and is_first_root_below_one(a, b, c):
			results.append((-b - sqrt(discriminant)) / (2*a))

		if is_second_root_nonnegative(a, b, c) and is_second_root_below_one(a, b, c):
			results.append((-b + sqrt(discriminant)) / (2*a))

		return results

	def starts_going_left(self):
		if self.p1.x == self.p0.x:
			return self.p2.x < self.p0.x
		else:
			return self.p1.x < self.p0.x

	def ends_going_left(self):
		if self.p1.x == self.p2.x:
			return self.p0.x > self.p2.x
		else:
			return self.p1.x > self.p2.x

	def get_side_vectors(self):
		return [self.p1 - self.p0, self.p2 - self.p1]

	def get_upright_coeffs(self, other): # Assumes that the axes are parallel
		c1, b1, a1 = self.get_coeff_vectors()
		c2, b2, a2 = other.get_coeff_vectors()

		if a1.x == 0: # If already upright
			return a1.y, b1.y, c1.y, b1.x, c1.x, a2.y, b2.y, c2.y, b2.x, c2.x

		return a1.x, b1.x, c1.x, b1.x * a1.y - b1.y * a1.x, c1.x * a1.y - c1.y * a1.x, \
		       a2.x, b2.x, c2.x, b2.x * a1.y - b2.y * a1.x, c2.x * a1.y - c2.y * a1.x

	def find_parallel_parabola_intersections(self, other):
		a1, b1, c1, d1, e1, a2, b2, c2, d2, e2 = self.get_upright_coeffs(other)

		e = e1 - e2
		a = a2*d1*d1 - a1*d2*d2
		b = d1*(2*a2*e + b2*d2) - b1*d2*d2
		c = a2*e*e + b2*d2*e + (c2 - c1)*d2*d2

		discriminant = b*b - 4*a*c
		if discriminant <= 0:
			return []

		if a == 0:
			t1 = -c / b
			if 0 <= t1 < 1:
				t2 = (d1*t1 + e) / d2
				if 0 <= t2 < 1:
					return [CurveIntersection(self, other, t1, t2)]
			return []

		results = []

		for sign in (-1, 1):
			t1 = (-b + sign * sqrt(discriminant)) / (2*a)
			if 0 <= t1 < 1:
				t2 = (d1*t1 + e) / d2
				if 0 <= t2 < 1:
					results.append(CurveIntersection(self, other, t1, t2))

		return results

	def find_intersections(self, other):
		if isinstance(other, LinearCurve):
			return other.find_parabolic_curve_intersections(self)

		# Construct a matrix for a linear map that makes the parabolas perpendicular
		m1 =   self.p0.y +  self.p2.y - 2 *  self.p1.y
		m2 = -other.p0.y - other.p2.y + 2 * other.p1.y
		m3 =  -self.p0.x -  self.p2.x + 2 *  self.p1.x
		m4 =  other.p0.x + other.p2.x - 2 * other.p1.x

		if m1 * m4 == m2 * m3:
			return self.find_parallel_parabola_intersections(other)

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

		line1 = LinearCurve(p0, p0 + self.derivative(t))
		line2 = LinearCurve(self.p2, self.p1)
		intersection = find_line_intersection(line1, line2, clip=False)

		if intersection is None:
			return LinearCurve(p0, self.p2)

		return make_curve(p0, intersection.get_pos(), self.p2)

	def clip_after(self, t):
		p2 = self.eval(t)

		line1 = LinearCurve(p2, p2 + self.derivative(t))
		line2 = LinearCurve(self.p0, self.p1)
		intersection = find_line_intersection(line1, line2, clip=False)

		if intersection is None:
			return LinearCurve(self.p0, p2)

		return make_curve(self.p0, intersection.get_pos(), p2)

	def clip_after_until(self, t1, t2):
		p0 = self.eval(t1)
		p2 = self.eval(t2)

		line1 = LinearCurve(p0, p0 + self.derivative(t1))
		line2 = LinearCurve(p2, p2 + self.derivative(t2))
		intersection = find_line_intersection(line1, line2, clip=False)

		if intersection is None:
			return LinearCurve(p0, p2)

		return make_curve(p0, intersection.get_pos(), p2)

	def transformed(self, f):
		return make_curve(f(self.p0), f(self.p1), f(self.p2))

def make_curve(p0, p1, p2):
	p0 = IntVec2(p0)
	p1 = IntVec2(p1)
	p2 = IntVec2(p2)

	if (p0.x - p1.x) * (p2.y - p1.y) == (p0.y - p1.y) * (p2.x - p1.x):
		return LinearCurve(p0, p2)
	else:
		return ParabolicCurve(p0, p1, p2)
