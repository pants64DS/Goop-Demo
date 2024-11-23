from util import IntVec

def _parabola_encloses(point, a, b, c, d, e, offset_times_two):
	x, y = 2 * point + offset_times_two
	f = a * x - b * y

	return f * f < (2 * (d * y - c * x) - 2 * e) * 2 * e

def leaning_curve_encloses_point(curve, point):
	p0 = curve.p0 - curve.p1
	p2 = curve.p2 - curve.p1
	point = IntVec(point) - curve.p1

	# if p0.x == -p2.x or p0.y == -p2.y:
	# 	return False
		# raise NotImplementedError("Coordinate-aligned parabolas")

	# Flip the axis of the parabola to the first quadrant
	if p0.x < -p2.x:
		p0.x = -p0.x
		p2.x = -p2.x
		point.x = -point.x

	if p0.y < -p2.y:
		p0.y = -p0.y
		p2.y = -p2.y
		point.y = -point.y

	a = p0.y + p2.y
	b = p0.x + p2.x
	c = p0.y - p2.y
	d = p0.x - p2.x
	e = p0.x * p2.y - p2.x * p0.y

	in_P0 = _parabola_encloses(point, a, b, c, d, e, IntVec(1, -1))
	in_P1 = _parabola_encloses(point, a, b, c, d, e, IntVec(-1, 1))

	if in_P0 and in_P1 and _parabola_encloses(point, a, b, c, d, e, IntVec(-1, -1)):
		return

	# Min x and min y
	if b * (2 * point.x + 1) <= 2 * p0.x * p2.x \
	or a * (2 * point.y + 1) <= 2 * p0.y * p2.y:
		return False

	# Top left parabola
	if b * (b * (2 * point.y - 1) - a * (2 * point.x + 1)) \
	>= 2 * d * e and not in_P0:
		return False

	# Bottom right parabola
	if a * (b * (2 * point.y + 1) - a * (2 * point.x - 1)) \
	<= 2 * c * e and not in_P1:
		return False

	# Bottom left parabola
	if a * (2 * point.x + 1) + b * (2 * point.y + 1) \
	<= 2 * (p0.x * p2.y + p2.x * p0.y) \
	and not _parabola_encloses(point, a, b, c, d, e, IntVec(1, 1)):
		return False

	return True

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

	def __contains__(self, point):
		return leaning_curve_encloses_point(self, point)

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
