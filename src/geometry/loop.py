import pyray
from util.vector2 import IntVec2
from geometry.curve import Curve

class Loop:
	def __init__(self, points):
		if len(points) & 1:
			raise ValueError("The number of points must be even")

		self.curves = []
		for i in range(1, len(points) - 1, 2):
			self.curves.append(Curve(points[i], points[i + 1], points[i + 2]))

		self.curves.append(Curve(points[-1], points[0], points[1]))

	def draw(self, color, thickness=2):
		for curve in self.curves:
			curve.draw(color)

		for curve in self.curves:
			curve.draw_lines(pyray.RED)

	# Assumes that the loops don't intersect
	def is_point_inside(self, point):
		line_x = point.x
		line_start_y = point.y
		parity = 0

		for curve in self.curves:
			x_coords = (curve.p0.x, curve.p1.x, curve.p2.x)
			y_coords = (curve.p0.y, curve.p1.y, curve.p2.y)

			left_bound_x   = min(x_coords)
			right_bound_x  = max(x_coords)
			bottom_bound_y = min(y_coords)
			top_bound_y    = max(y_coords)

			if top_bound_y <= line_start_y:
				parity += curve.parity_of_vertical_line_intersections(line_x)

			elif left_bound_x <= line_x <= right_bound_x and bottom_bound_y <= line_start_y:
				for y in curve.find_vertical_line_intersections(line_x):
					if y <= line_start_y:
						parity += 1

			if line_x == curve.p0.x and line_start_y > curve.p0.y:
				to_the_left = (curve.p1.x if curve.p1.x else curve.p2.x) < line_x

				if to_the_left:
					parity += 1

			if line_x == curve.p2.x and line_start_y > curve.p2.y:
				from_the_right = (curve.p1.x if curve.p1.x else curve.p0.x) > line_x

				if from_the_right:
					parity += 1

		return bool(parity & 1)

	def is_inside_nonintersecting(self, other):
		return other.is_point_inside(self.curves[0].p0)

	def is_outside_nonintersecting(self, other):
		return not self.is_inside_nonintersecting(other)

	def is_separate_nonintersecting(self, other):
		return self.is_outside_nonintersecting(other) \
		and other.is_outside_nonintersecting(self)
