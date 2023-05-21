
class BoundingBox:
	def __init__(self, *points):
		x_coords = [p.x for p in points]
		y_coords = [p.y for p in points]

		self.left_x   = min(x_coords)
		self.right_x  = max(x_coords)
		self.bottom_y = min(y_coords)
		self.top_y    = max(y_coords)

class CurveIntersection:
	def __init__(self, curve1, curve2, t1, t2):
		self.curve1 = curve1
		self.curve2 = curve2
		self.t1 = t1
		self.t2 = t2

	def get_pos(self, on_curve1=True):
		if on_curve1:
			return self.curve1.eval(self.t1)
		else:
			return self.curve2.eval(self.t2)
