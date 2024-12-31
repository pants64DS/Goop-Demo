from util import IntVec, det
from sympy import symbols
from sympy.polys.polytools import Poly, count_roots

def curve_intersects_parabola(p0, p1, p2, q0, q1, q2):
	pass

def curve_intersection(p0, p1, p2, q0, q1, q2):
	t = symbols("t")
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
		if (det(g, p1 - p0) < 0) ^ (det(g, f) < 0):
			return 1, False
		else:
			return 2, None

	return -1, None
