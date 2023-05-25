from util import IntVec

class CurvePointCollision:
	def __init__(self, curve, point):
		self.p0 = curve.p0 - curve.p1
		self.p2 = curve.p2 - curve.p1
		self.point = IntVec(point) - curve.p1

		# if self.p0.x == -self.p2.x or self.p0.y == -self.p2.y:
		# 	return False
			# raise NotImplementedError("Coordinate-aligned parabolas")

		# Flip the axis of the parabola to the first quadrant
		if self.p0.x < -self.p2.x:
			self.p0.x = -self.p0.x
			self.p2.x = -self.p2.x
			self.point.x = -self.point.x

		if self.p0.y < -self.p2.y:
			self.p0.y = -self.p0.y
			self.p2.y = -self.p2.y
			self.point.y = -self.point.y

		self.a = self.p0.y + self.p2.y
		self.b = self.p0.x + self.p2.x
		self.c = self.p0.y - self.p2.y
		self.d = self.p0.x - self.p2.x
		self.e = self.p0.x * self.p2.y - self.p2.x * self.p0.y

	def _parabola_encloses(self, x, y):
		f = self.a * x - self.b * y

		return f * f < (2 * (self.d * y - self.c * x) - self.e) * self.e

	def middle_edge_encloses_point(self):
		return self._parabola_encloses(*self.point)

	def inner_edge_encloses_point(self, edge_dist):
		x = self.point.x - edge_dist
		y = self.point.y + edge_dist

		if self._parabola_encloses(x, y):
			y -= edge_dist * 2
			if self._parabola_encloses(x, y):
				x += edge_dist * 2
				if self._parabola_encloses(x, y):
					return True

		return False

	def outer_edge_encloses_point(self, edge_dist):
		# Min x and min y
		x = self.point.x + edge_dist
		y = self.point.y + edge_dist

		if self.b * x <= self.p0.x * self.p2.x or self.a * y <= self.p0.y * self.p2.y:
			return False

		# Top left parabola
		y -= edge_dist * 2

		f = self.b * y - self.a * x
		if self.b * f >= self.d * self.e and not self._parabola_encloses(x, y):
			return False

		# Bottom right parabola
		x -= edge_dist * 2
		y += edge_dist * 2

		f = self.b * y - self.a * x
		if self.a * f <= self.c * self.e and not self._parabola_encloses(x, y):
			return False

		# Bottom left parabola
		x += edge_dist * 2

		if self.a * x + self.b * y <= self.p0.x * self.p2.y + self.p2.x * self.p0.y \
		and not self._parabola_encloses(x, y):
			return False

		return True

	def edge_encloses_point(self, edge_id):
		if edge_id < 0:
			return self.inner_edge_encloses_point(-edge_id)

		if edge_id > 0:
			return self.outer_edge_encloses_point(edge_id)

		return self.middle_edge_encloses_point()

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

	def inner_curve_contains(self, point):
		clsn = CurvePointCollision(self, point)

		return clsn.middle_edge_encloses_point() and not clsn.inner_edge_encloses_point(1)

	def __contains__(self, point):
		clsn = CurvePointCollision(self, point)

		return clsn.outer_edge_encloses_point(1) and not clsn.middle_edge_encloses_point()

	def outer_curve_contains(self, point):
		clsn = CurvePointCollision(self, point)

		return clsn.outer_edge_encloses_point(2) and not clsn.outer_edge_encloses_point(1)

	def curve_contains(self, point, curve_id):
		clsn = CurvePointCollision(self, point)

		return clsn.edge_encloses_point(curve_id + 1) and not clsn.edge_encloses_point(curve_id)
