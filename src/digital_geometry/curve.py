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

def point_in_discrete_curve(u, p0, p1, p2):
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
	s5 = -s1*s2*s3
	s6 = sgn(s4*(a1*b2 - a2*b1)**2 - s3*(a2*a2*d1 + a1*a1*d2))

	return 4*s5*a1*a1*a2*a2*d1*d2 \
		< s6*(s4*(a1*b2 - a2*b1)**2 - s3*(a2*a2*d1 + a1*a1*d2))**2

def root_intervals_overlap(start1, end1, start2, end2):
	return not (root_is_less_than(*end2, *start1) or root_is_less_than(*end1, *start2))

def point_in_discrete_curve_2(u, p0, p1, p2):
	p0 = p0 - u
	p1 = p1 - u
	p2 = p2 - u

	a1, a2 = 2*(p0 + p2 - 2*p1)
	b1, b2 = 4*(p1 - p0)
	c1, c2 = 2*(p0)

	if a1 < 0: a1, b1, c1 = -a1, -b1, -c1
	if a2 < 0: a2, b2, c2 = -a2, -b2, -c2

	d1 = b1*b1 - 4*a1*(c1 - 1)
	if d1 < 0: return False

	d2 = b2*b2 - 4*a2*(c2 - 1)
	if d2 < 0: return False

	D1 = b1*b1 - 4*a1*(c1 + 1)
	D2 = b2*b2 - 4*a2*(c2 + 1)

	outer_left_f1  = a1, b1, d1, -1
	inner_left_f1  = a1, b1, D1, -1
	outer_right_f1 = a1, b1, d1, +1
	inner_right_f1 = a1, b1, D1, +1

	outer_left_f2  = a2, b2, d2, -1
	inner_left_f2  = a2, b2, D2, -1
	outer_right_f2 = a2, b2, d2, +1
	inner_right_f2 = a2, b2, D2, +1

	if D1 > 0:
		# two strip segments to check
		# check if the strip segments of the first parabola overlap with them

		if D2 > 0:
			# two strip segments to check against two other strip segments
			return (
				root_intervals_overlap(outer_left_f1,  inner_left_f1,  outer_left_f2,  inner_left_f2)  or
				root_intervals_overlap(outer_left_f1,  inner_left_f1,  inner_right_f2, outer_right_f2) or
				root_intervals_overlap(inner_right_f1, outer_right_f1, outer_left_f2,  inner_left_f2)  or
				root_intervals_overlap(inner_right_f1, outer_right_f1, inner_right_f2, outer_right_f2)
			)

		# two strip segments to check against one strip segment
		return (
			root_intervals_overlap(outer_left_f1,  inner_left_f1,  outer_left_f2, outer_right_f2) or
			root_intervals_overlap(inner_right_f1, outer_right_f1, outer_left_f2, outer_right_f2)
		)

	# one strip segment to check
	# check if the strip segments of the first parabola overlap with it

	if D2 > 0:
		# one strip segment to check against two strip segments
		return (
			root_intervals_overlap(outer_left_f1, outer_right_f1, outer_left_f2,  inner_left_f2) or
			root_intervals_overlap(outer_left_f1, outer_right_f1, inner_right_f2, outer_right_f2)
		)

	# one strip segment to check against one strip segment
	return root_intervals_overlap(outer_left_f1, outer_right_f1, outer_left_f2, outer_right_f2)

def dfs_in_discrete_curve(u, p0, p1, p2, visited):
	if u in visited: return
	visited.add(u)

	if not point_in_discrete_curve(u, p0, p1, p2):
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
		return point_in_discrete_curve(IntVec(point), self.p0, self.p1, self.p2)

	def __iter__(self):
		yield from dfs_in_discrete_curve(self.p0, self.p0, self.p1, self.p2, set())
