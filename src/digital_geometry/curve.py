from util import IntVec

def parabola_encloses(a, b, c, d, e, u, offset_times_two):
	x, y = 2 * u + offset_times_two
	f = a * x - b * y

	return f * f < (2 * (d * y - c * x) - 2 * e) * 2 * e

def point_before_control_point(u, p, u_in_P0, u_in_P1, u_in_P2):
	# If p is in the first quadrant
	if p.x >= 0 and p.y >= 0:
		return (
			u_in_P0 and not u_in_P1
			and (u.y > p.y or (u.y == p.y and u.x > p.x))
		)

	# If p is in the third quadrant
	if p.x <= 0 and p.y <= 0:
		return (
			(u_in_P0 and not u_in_P1)
			or u.x < p.x or (u.x == p.x and u.y < p.y)
		)

	# If p is in the second quadrant
	return (
		(u_in_P0 and (u_in_P2 or u.y > p.y))
		or u.x < p.x or (u.x == p.x and u.y > p.y)
	)

def point_in_discrete_curve(u, p0, p1, p2):
	p0 -= p1
	p2 -= p1
	u  -= p1

	# if p0.x == -p2.x or p0.y == -p2.y:
	# 	return False
		# raise NotImplementedError("Coordinate-aligned parabolas")

	# Flip the axis of the parabola to the first quadrant
	if p0.x < -p2.x:
		p0.x = -p0.x
		p2.x = -p2.x
		u.x = -u.x

	if p0.y < -p2.y:
		p0.y = -p0.y
		p2.y = -p2.y
		u.y = -u.y

	# Mirror the curve along the diagonal to make it turn counterclockwise
	if p0.x * p2.y > p0.y * p2.x:
		p0.x, p0.y = p0.y, p0.x
		p2.x, p2.y = p2.y, p2.x
		u.x, u.y = u.y, u.x

	a = p0.y + p2.y
	b = p0.x + p2.x
	c = p0.y - p2.y
	d = p0.x - p2.x
	e = p0.x * p2.y - p2.x * p0.y

	u_in_P0 = parabola_encloses(a, b, c, d, e, u, IntVec(1, -1))
	u_in_P1 = parabola_encloses(a, b, c, d, e, u, IntVec(-1, 1))
	u_in_P2 = parabola_encloses(a, b, c, d, e, u, IntVec(-1, -1))
	u_in_P3 = parabola_encloses(a, b, c, d, e, u, IntVec(1, 1))

	if u_in_P0 and u_in_P1 and u_in_P2:
		return

	# Min x and min y
	if b * (2 * u.x + 1) <= 2 * p0.x * p2.x \
	or a * (2 * u.y + 1) <= 2 * p0.y * p2.y:
		return False

	# Top left parabola
	if not u_in_P0 and b * (b * (2 * u.y - 1) - a * (2 * u.x + 1)) >= 2 * d * e:
		return False

	# Bottom right parabola
	if not u_in_P1 and a * (b * (2 * u.y + 1) - a * (2 * u.x - 1)) <= 2 * c * e:
		return False

	# Bottom left parabola
	if not u_in_P3 and a * (2 * u.x + 1) + b * (2 * u.y + 1) <= 2 * (p0.x * p2.y + p2.x * p0.y):
		return False

	# Check if point u is between the endpoints
	if point_before_control_point(u, p0, u_in_P0, u_in_P1, u_in_P2):
		return False

	if point_before_control_point(IntVec(u.y, u.x), IntVec(p2.y, p2.x), u_in_P1, u_in_P0, u_in_P2):
		return False

	return u.x <= max(p0.x, p2.x) and u.y <= max(p0.y, p2.y)

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

	def __contains__(self, point):
		return point_in_discrete_curve(IntVec(point), self.p0, self.p1, self.p2)

	def search(self, point, visited):
		if point in visited: return
		visited.add(point)

		if point not in self or abs(point.x) > 50 or abs(point.y) > 50:
			return
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
