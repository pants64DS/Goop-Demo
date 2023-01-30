from util.vector2 import Vector2
import pyray

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = p0
		self.p1 = p1
		self.p2 = p2

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
