from util import IntVec

class Curve:
	def __init__(self, p0, p1, p2):
		self.p0 = IntVec(p0)
		self.p1 = IntVec(p1)
		self.p2 = IntVec(p2)

	def is_in_bounded_area(self, v):
		p0 = self.p0 - self.p1
		p2 = self.p2 - self.p1
		x, y = v - self.p1

		a = p0.y + p2.y
		b = p0.x + p2.x
		c = p0.y - p2.y
		d = p0.x - p2.x
		e = p0.x * p2.y - p2.x * p0.y

		return (a * x - b * y)**2 < (2 * (d * y - c * x) - e) * e

	def inner_curve_contains(self, v):
		p0 = self.p0 - self.p1
		p2 = self.p2 - self.p1
		x, y = IntVec(v) - self.p1

		# Flip the axis of the parabola to the first quadrant
		if p0.x < -p2.x:
			p0.x = -p0.x
			p2.x = -p2.x
			x = -x

		if p0.y < -p2.y:
			p0.y = -p0.y
			p2.y = -p2.y
			y = -y

		a = p0.y + p2.y
		b = p0.x + p2.x
		c = p0.y - p2.y
		d = p0.x - p2.x
		e = p0.x * p2.y - p2.x * p0.y

		if (a * x - b * y)**2 >= (2 * (d * y - c * x) - e) * e:
			return False

		x -= 1
		y += 1
		if (a * x - b * y)**2 < (2 * (d * y - c * x) - e) * e:
			y -= 2
			if (a * x - b * y)**2 < (2 * (d * y - c * x) - e) * e:
				x += 2
				if (a * x - b * y)**2 < (2 * (d * y - c * x) - e) * e:
					return False

		return True

	def __contains__(self, v):
		p0 = self.p0 - self.p1
		p2 = self.p2 - self.p1
		x, y = IntVec(v) - self.p1

		# if p0.x == -p2.x or p0.y == -p2.y:
		# 	return False
			# raise NotImplementedError("Coordinate-aligned parabolas")

		# Flip the axis of the parabola to the first quadrant
		if p0.x < -p2.x:
			p0.x = -p0.x
			p2.x = -p2.x
			x = -x

		if p0.y < -p2.y:
			p0.y = -p0.y
			p2.y = -p2.y
			y = -y

		a = p0.y + p2.y
		b = p0.x + p2.x
		c = p0.y - p2.y
		d = p0.x - p2.x
		e = p0.x * p2.y - p2.x * p0.y

		if b * (x + 1) <= p0.x * p2.x or a * (y + 1) <= p0.y * p2.y:
			return False

		if (a * x - b * y)**2 < (2 * (d * y - c * x) - e) * e:
			return False

		x += 1
		y -= 1

		f = b * y - a * x
		if b * f >= d * e:
			if f * f >= (2 * (d * y - c * x) - e) * e:
				return False

		x -= 2
		y += 2

		f = b * y - a * x
		if a * f <= c * e:
			if f * f >= (2 * (d * y - c * x) - e) * e:
				return False

		x += 2

		if a * x + b * y <= p0.x * p2.y + p2.x * p0.y:
			if (b * y - a * x)**2 >= (2 * (d * y - c * x) - e) * e:
				return False

		return True
