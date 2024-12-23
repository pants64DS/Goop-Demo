from util import IntVec

def parabola_encloses(a, b, c, d, e, u, offset_times_two):
	x, y = 2 * u + offset_times_two
	f = a * x - b * y

	return f * f < (2 * (d * y - c * x) - 2 * e) * 2 * e

def point_before_endpoint(u, p0, u_in_P0, u_in_P1, u_in_P2):
	# If p0 is in the first quadrant
	if p0.x >= 0 and p0.y >= 0:
		return (
			u_in_P0 and not u_in_P1
			and (u.y > p0.y or (u.y == p0.y and u.x > p0.x))
		)

	# If p0 is in the third quadrant
	if p0.x <= 0 and p0.y <= 0:
		return (
			(u_in_P0 and not u_in_P1)
			or u.x < p0.x or (u.x == p0.x and u.y < p0.y)
		)

	# If p0 is in the second quadrant
	return (
		(u_in_P0 and (u_in_P2 or u.y > p0.y))
		or u.x < p0.x or (u.x == p0.x and u.y > p0.y)
	)

def point_in_discrete_curve_1(u, p0, p1, p2):
	p0 -= p1
	p2 -= p1
	u  -= p1

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
	if point_before_endpoint(u, p0, u_in_P0, u_in_P1, u_in_P2):
		return False

	if point_before_endpoint(IntVec(u.y, u.x), IntVec(p2.y, p2.x), u_in_P1, u_in_P0, u_in_P2):
		return False

	return u.x <= max(p0.x, p2.x) and u.y <= max(p0.y, p2.y)

# ====================================================================================

def sgn(x):
	if x < 0: return -1
	if x > 0: return 1
	return 0

def root_is_less_than(a1, b1, d1, s1, a2, b2, d2, s2):
	s3 = sgn(s1*a2*a2*d1 - s2*a1*a1*d2)
	s4 = sgn(a2*b1 - a1*b2)
	s5 = sgn(s4*(a1*b2 - a2*b1)**2 - s3*(a2*a2*d1 + a1*a1*d2))

	return -4*s1*s2*s3*a1*a1*a2*a2*d1*d2 \
		< s5*(s4*(a1*b2 - a2*b1)**2 - s3*(a2*a2*d1 + a1*a1*d2))**2

def root_intervals_overlap(start1, end1, start2, end2):
	return not (root_is_less_than(*end1, *start2) or root_is_less_than(*end2, *start1))

def get_strip_intervals(a, b, c):
	if a == 0:
		if b == 0:
			if c == 0:
				return [((1, 0, 0, 1), (1, 0, 4, 1))]
			else:
				return []

		if b < 0: b, c = -b, -c

		return [((b, 2*c, 1, -1), (b, 2*c, 1, +1))]

	if a < 0: a, b, c = -a, -b, -c

	d1 = b*b - 2*a*(2*c - 1)
	if d1 < 0: return []

	d2 = b*b - 2*a*(2*c + 1)

	outer_left  = a, b, d1, -1
	outer_right = a, b, d1, +1

	if d2 <= 0: return [(outer_left, outer_right)]

	inner_left  = a, b, d2, -1
	inner_right = a, b, d2, +1

	return [(outer_left,  inner_left), (inner_right, outer_right)]

def root_below_zero(a, b, d, s):
	return s*d < sgn(b)*b*b

def root_above_one(a, b, d, s):
	h = 2*a + b
	return s*d > sgn(h)*h*h

def get_clipped_intervals(a, b, c):
	clipped_intervals = []

	for start, end in get_strip_intervals(a, b, c):
		if root_below_zero(*end) or root_above_one(*start): continue
		if root_below_zero(*start): start = 1, 0, 0, 1
		if root_above_one(*end):    end   = 1, 0, 4, 1

		clipped_intervals.append((start, end))

	return clipped_intervals

def point_in_discrete_curve_2(u, p0, p1, p2):
	a1, a2 = p0 + p2 - 2*p1
	b1, b2 = 2*(p1 - p0)
	c1, c2 = p0 - u

	for i1 in get_clipped_intervals(a1, b1, c1):
		for i2 in get_clipped_intervals(a2, b2, c2):
			if root_intervals_overlap(*i1, *i2):
				return True

	return False

# ====================================================================================

def point_in_discrete_curve_3(u, p0, p1, p2):
	if p0 == p1 == p2: return u == p0

	a = p0 + p2 - 2*p1
	b = 2*(p1 - p0)
	c = p0 - u

	for i in 0, 1:
		if a[i] < 0 or (a[i] == 0 and b[i] < 0):
			a[i], b[i], c[i] = -a[i], -b[i], -c[i]

	for i in 0, 1:
		j = 1 - i
		a1, b1, c1 = a[i], b[i], c[i]
		a2, b2, c2 = a[j], b[j], c[j]

		if a1 == 0:
			for s1 in -1, 1:
				d1 = s1 - 2*c1
				if 0 <= d1 <= 2*b1 and \
				   0 <= a2*d1**2 + 2*b1*(b1*(2*c2 + 1) + b2*d1) <= 4*b1*b1:
						return True
			continue

		A = a1*a1
		B0 = a1*(2*a2*c1 - a1*(2*c2 + 1) + b1*b2) - a2*b1*b1
		s2 = sgn(a1*b2 - a2*b1)

		for s1 in -1, 1:
			d1 = b1*b1 - 2*a1*(2*c1 - s1)
			if d1 < 0: continue

			B = B0 - a1*a2*s1
			D = d1*(a1*b2 - a2*b1)**2

			for s3 in -1, 1:
				if  not root_below_zero(a1, b1, d1, s3) \
				and not root_above_one (a1, b1, d1, s3) \
				and not root_below_zero(A, B, D, s2*s3) \
				and not root_above_one (A, B, D, s2*s3):
					return True
	return False

# ====================================================================================

def dfs_in_discrete_curve(u, p0, p1, p2, visited):
	if u in visited: return
	visited.add(u)

	if not point_in_discrete_curve_3(u, p0, p1, p2):
		return

	yield u

	yield from dfs_in_discrete_curve(IntVec(u.x + 1, u.y), p0, p1, p2, visited)
	yield from dfs_in_discrete_curve(IntVec(u.x - 1, u.y), p0, p1, p2, visited)
	yield from dfs_in_discrete_curve(IntVec(u.x, u.y + 1), p0, p1, p2, visited)
	yield from dfs_in_discrete_curve(IntVec(u.x, u.y - 1), p0, p1, p2, visited)

	return visited

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

	def __contains__(self, point):
		return point_in_discrete_curve_3(IntVec(point), self.p0, self.p1, self.p2)

	def __iter__(self):
		yield from dfs_in_discrete_curve(self.p0, self.p0, self.p1, self.p2, set())
