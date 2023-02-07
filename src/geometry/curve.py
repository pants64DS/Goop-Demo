import numpy
import pyray
from util.vector2 import IntVec2

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec2(p0)
		self.p1 = IntVec2(p1)
		self.p2 = IntVec2(p2)

	def get_coeff_vectors(self):
		return self.p0, 2 * (self.p1 - self.p0), self.p0 + self.p2 - 2 * self.p1

	def get_x_coeffs(self):
		return self.p0.x, 2 * (self.p1.x - self.p0.x), self.p0.x + self.p2.x - 2 * self.p1.x

	def get_y_coeffs(self):
		return self.p0.y, 2 * (self.p1.y - self.p0.y), self.p0.y + self.p2.y - 2 * self.p1.y

	def eval(self, t):
		coeffs = self.get_coeff_vectors()

		return coeffs[0] + (coeffs[1] + coeffs[2] * t) * t

	def draw(self, color, thickness=2):
		pyray.draw_line_bezier_quad(
			self.p0.to_pyray_vector2(),
			self.p2.to_pyray_vector2(),
			self.p1.to_pyray_vector2(),
			thickness, color
		)

	def find_intersections(self, other):
		# Construct a matrix for a linear map that makes the parabolas perpendicular
		m1 =   self.p0.y +  self.p2.y - 2 *  self.p1.y
		m2 = -other.p0.y - other.p2.y + 2 * other.p1.y
		m3 =  -self.p0.x -  self.p2.x + 2 *  self.p1.x
		m4 =  other.p0.x + other.p2.x - 2 * other.p1.x

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
		for root in f.roots():
			t = numpy.real(root)
			if abs(numpy.imag(root)) < 1e-5 and 0 <= t <= 1:
				lo, hi = sorted((q0y, q2y))
				if lo <= (a1*t + b1) * t + p0y <= hi:
					results.append(self.eval(t))

		return results
