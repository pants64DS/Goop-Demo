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

	def _parabola_encloses(self, offset_times_two):
		x, y = 2 * self.point + offset_times_two

		return (self.a * x - self.b * y)**2 \
		< (2 * (self.d * y - self.c * x) - 2 * self.e) * 2 * self.e

	def inner_edge_encloses_point(self):
		return self._parabola_encloses(IntVec(-1, 1)) \
		and    self._parabola_encloses(IntVec(-1, -1)) \
		and    self._parabola_encloses(IntVec(1, -1))

	def outer_edge_encloses_point(self, edge_dist=1):
		# Min x and min y
		if self.b * (2 * self.point.x + edge_dist) <= 2 * self.p0.x * self.p2.x \
		or self.a * (2 * self.point.y + edge_dist) <= 2 * self.p0.y * self.p2.y:
			return False

		# Top left parabola
		y = self.point.y - edge_dist

		if self.b * (self.b * (2 * self.point.y - edge_dist) - self.a * (2 * self.point.x + edge_dist)) \
		>= 2 * self.d * self.e \
		and not self._parabola_encloses(IntVec(1, -1)):
			return False

		# Bottom right parabola
		if self.a * (self.b * (2 * self.point.y + edge_dist) - self.a * (2 * self.point.x - edge_dist)) \
		<= 2 * self.c * self.e \
		and not self._parabola_encloses(IntVec(-1, 1)):
			return False

		# Bottom left parabola
		if self.a * (2 * self.point.x + edge_dist) + self.b * (2 * self.point.y + edge_dist) \
		<= 2 * (self.p0.x * self.p2.y + self.p2.x * self.p0.y) \
		and not self._parabola_encloses(IntVec(1, 1)):
			return False

		return True

	def get_region_id(self):
		x, y = self.point

		# Tip
		if self.a * x + self.b * y <= self.p0.x * self.p2.y + self.p2.x * self.p0.y:
			return 1

		# Before tip
		if self.b * (self.b * y - self.a * x) >= self.d * self.e:
			return 0

		# After tip
		return 2

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

		self.order = self.get_order(self.p0, self.p2)

	def extended_curve_contains(self, point):
		clsn = CurvePointCollision(self, point)

		return clsn.outer_edge_encloses_point() and not clsn.inner_edge_encloses_point()

	def __contains__(self, point):
		return self.extended_curve_contains(point)

		"""
		return self.extended_curve_contains(point) \
			and not self.comes_before(point, self.p0) \
			and not self.comes_before(self.p2, point)
		"""

	def comes_before(self, point1, point2):
		return self.order * self.get_order(point1, point2) > 0

	def get_order(self, point1, point2):
		clsn1 = CurvePointCollision(self, point1)
		clsn2 = CurvePointCollision(self, point2)

		region1 = clsn1.get_region_id()
		region2 = clsn2.get_region_id()

		if region1 != region2:
			return region1 - region2

		if clsn1.point.x != clsn2.point.x:
			if region1 == 0:
				return clsn2.point.x - clsn1.point.x
			else:
				return clsn1.point.x - clsn2.point.x
		else:
			if region1 == 2:
				return clsn1.point.y - clsn2.point.y
			else:
				return clsn2.point.y - clsn1.point.y

	def get_next_point(self, point):
		res = None

		for i in range(4):
			j = i >> 1 & 1
			offset = IntVec(j - (i & 1), j - (~i & 1))
			adjacent_point = point + offset

			if self.extended_curve_contains(adjacent_point) \
			and self.comes_before(point, adjacent_point) \
			and (res is None or not self.comes_before(res, adjacent_point)):
				res = adjacent_point

		return res

	def in_bounding_box(self, point):
		min_x, _, max_x = sorted([self.p0.x, self.p1.x, self.p2.x])
		min_y, _, max_y = sorted([self.p0.y, self.p1.y, self.p2.y])

		return min_x <= point.x <= max_x and min_y <= point.y <= max_y

	def search(self, point, visited):
		if point in visited: return
		visited.add(point)

		if point not in self or not self.in_bounding_box(point): return
		yield point

		yield from self.search(IntVec(point.x + 1, point.y), visited)
		yield from self.search(IntVec(point.x - 1, point.y), visited)
		yield from self.search(IntVec(point.x, point.y + 1), visited)
		yield from self.search(IntVec(point.x, point.y - 1), visited)

		return visited

	def __iter__(self):
		try:
			yield from self.search(self.p0, set())
		except Exception as e:
			print(f"ERROR!!!!!!: {e}")

		"""
		while True:
			yield point

			if point == self.p2:
				break

			point = self.get_next_point(point)

			# The next point might not exist if the curve is degenerate
			if point is None: raise Exception("The next point on the curve doesn't exist")
		"""