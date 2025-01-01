from util import IntVec, det
from sympy import symbols
from sympy.polys.polytools import Poly, count_roots

t = symbols("t")

def count_curve_parabola_intersections(p0, p1, p2, q0, q1, q2):
	a = p0 + p2 - 2*p1
	b = 2*(p1 - p0)
	c = p0 - q1
	d = det(q0 - q1, q2 - q1)
	u = q0 + q2 - 2*q1
	v = q0 - q2

	x = a[0]*t**2 + b[0]*t + c[0]
	y = a[1]*t**2 + b[1]*t + c[1]

	P = Poly((u[1]*x - u[0]*y)**2 + d*(2*(v[1]*x - v[0]*y) + d))
	return count_roots(P, inf=0, sup=1)

def curve_intersection(p0, p1, p2, q0, q1, q2):
	if det(p1 - p0, p2 - p0) < 0:
		p0, p2 = p2, p0

	d = q0 + q2 - 2*q1
	e = 2*(q1 - q0)
	f = q0 - p0
	g = p2 - p0

	# By the multilinearity of the determinant,
	#   det(d*t**2 + e*t + f, g)
	# = det(d, g)*t**2 + det(e, g)*t + det(f, g)

	P = Poly(det(d, g)*t**2 + det(e, g)*t + det(f, g))

	# If the second curve doesn't intersect the line
	if count_roots(P, inf=0, sup=1) == 0:
		# If the curves are on different sides of the line
		if det(g, f) > 0:
			return 1, False
		else:
			return 2, count_curve_parabola_intersections(q0, q1, q2, p0, p1, p2) != 0

	# If neither endpoint of the second curve is on
	# the same side of the line as the first curve
	if det(q0 - p0, g) <= 0 and det(q2 - p0, g) <= 0:
		return 3, count_curve_parabola_intersections(p0, p1, p2, q0, q1, q2) != 0

	return -1, None
