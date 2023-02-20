from math import floor, ceil
import pyray
from numpy import sign
from util.vector2 import IntVec2, get_angle_between
from geometry.curve import Curve, CurveIntersection

test_intersections = []

class Loop:
	# turning_number should be 1 if the curve is
	# counterclockwise, and -1 if the curve is clockwise,
	# or None if it isn't known
	def __init__(self, curves, turning_number=None):
		self.curves = curves

		if turning_number is None:
			self.turning_number = self.calculate_turning_number()
		else:
			self.turning_number = turning_number

	def eval(self, t):
		index = floor(t)
		return self.curves[index].eval(t - index)

	def derivative(self, t):
		index = floor(t)
		return self.curves[index].derivative(t - index)

	@classmethod
	def from_points(cls, points):
		if len(points) & 1:
			raise ValueError("The number of points must be even")

		curves = []
		for i in range(1, len(points) - 1, 2):
			curves.append(Curve(points[i], points[i + 1], points[i + 2]))

		curves.append(Curve(points[-1], points[0], points[1]))

		return cls(curves)

	def draw(self, color, thickness=2):
		for curve in self.curves:
			curve.draw(color)

	def draw_lines(self):
		for curve in self.curves:
			curve.draw_lines(pyray.RED)

	# Assumes that the loops don't intersect
	def is_point_inside(self, point):
		line_x = point.x
		line_start_y = point.y
		parity = 0

		for curve in self.curves:
			x_coords = (curve.p0.x, curve.p1.x, curve.p2.x)
			y_coords = (curve.p0.y, curve.p1.y, curve.p2.y)

			left_bound_x   = min(x_coords)
			right_bound_x  = max(x_coords)
			bottom_bound_y = min(y_coords)
			top_bound_y    = max(y_coords)

			if top_bound_y <= line_start_y:
				parity += curve.parity_of_vertical_line_intersections(line_x)

			elif left_bound_x <= line_x <= right_bound_x and bottom_bound_y <= line_start_y:
				for y in curve.find_vertical_line_intersections(line_x):
					if y <= line_start_y:
						parity += 1

			if line_x == curve.p0.x and line_start_y > curve.p0.y:
				to_the_left = (curve.p1.x if curve.p1.x else curve.p2.x) < line_x

				if to_the_left:
					parity += 1

			if line_x == curve.p2.x and line_start_y > curve.p2.y:
				from_the_right = (curve.p1.x if curve.p1.x else curve.p0.x) > line_x

				if from_the_right:
					parity += 1

		return bool(parity & 1)

	def is_inside_nonintersecting(self, other):
		return other.is_point_inside(self.curves[0].p0)

	def is_outside_nonintersecting(self, other):
		return not self.is_inside_nonintersecting(other)

	def is_separate_nonintersecting(self, other):
		return self.is_outside_nonintersecting(other) \
		and other.is_outside_nonintersecting(self)

	def intersects_with(self, other):
		for curve1 in self.curves:
			for curve2 in other.curves:
				if curve1.find_intersections(curve2):
					return True

		return False

	def calculate_turning_angle(self):
		angle = 0.0

		if not self.curves:
			return angle

		side_vectors = []
		for curve in self.curves:
			side_vectors.append(curve.p1 - curve.p0)
			side_vectors.append(curve.p2 - curve.p1)

		for i in range(len(side_vectors) - 1):
			angle += get_angle_between(side_vectors[i], side_vectors[i + 1])

		angle += get_angle_between(side_vectors[-1], side_vectors[0])

		return angle

	def calculate_turning_number(self):
		return sign(self.calculate_turning_angle())

	@staticmethod
	def get_intersections_between(loop1, loop2):
		results = []

		for curve1_id, curve1 in enumerate(loop1.curves):
			for curve2_id, curve2 in enumerate(loop2.curves):
				for curve_intersection in curve1.find_intersections(curve2):
					results.append(LoopIntersection(curve_intersection, loop1, loop2, curve1_id, curve2_id))

		return sorted(results, key=lambda intersection: intersection.params[1])

	def get_intersections(self, other_loops):
		intersections_by_loop = []
		all_intersections = []

		for other in other_loops:
			new_intersections = Loop.get_intersections_between(self, other)
			all_intersections += new_intersections
			intersections_by_loop.append(new_intersections)

		all_intersections.sort(key=lambda intersection: intersection.params[0])

		for i in range(len(all_intersections)):
			if all_intersections[i].get_next_loop() is self:
				next_index = (i + 1) % len(all_intersections)

				all_intersections[i].next_intersection = all_intersections[next_index]

		for loop, intersections in zip(other_loops, intersections_by_loop):
			for i in range(len(intersections)):
				if intersections[i].get_next_loop() is loop:
					next_index = (i + 1) % len(intersections)

					intersections[i].next_intersection = intersections[next_index]

		print(f"intersections_by_loop: {intersections_by_loop}")
		print(f"all_intersections: {all_intersections}")

		global test_intersections
		test_intersections += all_intersections
		return all_intersections

	def merge_to(self, loops):
		if not loops:
			return self, []

		intersections = self.get_intersections(loops)

		# result_loops = []
		new_loop = Loop([], 0)

		loops.append(self)

		first_intersection = intersections[0]
		intersection = first_intersection

		while True:
			print("-----------------")
			print(f"curr intersection: {intersection}")
			print(f"next intersection: {intersection.next_intersection}")

			start = intersection.params[intersection.next_loop_id]
			end = intersection.next_intersection.params[intersection.next_loop_id]

			# start, end = sorted([start, end])

			print(f"start: {start}")
			print(f"end:   {end}")

			new_loop.curves += intersection.get_next_loop().clip_interval(start, end)
			intersection = intersection.next_intersection

			if intersection is first_intersection:
				break

		new_loop.turning_number = new_loop.calculate_turning_number()
		return new_loop, []

	def clip_interval(self, start, end):
		if start == end:
			return []

		print(f"clipping an interval from {start} to {end}")

		start_curve_id = floor(start)
		end_curve_id = ceil(end) - 1

		t1 = start - start_curve_id
		t2 = end - end_curve_id

		print(f"start_curve_id: {start_curve_id}")
		print(f"end_curve_id:   {end_curve_id}")
		print(f"t1:             {t1}")
		print(f"t2:             {t2}")

		if start_curve_id == end_curve_id and t1 < t2:
			print("using clip_after_until")
			return [self.curves[start_curve_id].clip_after_until(t1, t2)]

		new_curves = [self.curves[start_curve_id].clip_until(t1)]

		curve_id = (start_curve_id + 1) % len(self.curves)
		while curve_id != end_curve_id:
			new_curves.append(self.curves[curve_id])
			curve_id = (curve_id + 1) % len(self.curves)

		new_curves.append(self.curves[end_curve_id].clip_after(t2))

		print(f"{len(new_curves)} curves added")
		return new_curves

class LoopIntersection:
	def __init__(self, curve_intersection, loop1, loop2, curve1_id, curve2_id):
		self.params = (curve1_id + curve_intersection.t1, curve2_id + curve_intersection.t2)
		self.loops = (loop1, loop2)

		self.set_next_loop_id()
		self.next_intersection = None

	def draw(self, color):
		pos = self.loops[0].eval(self.params[0])
		assert pos.dist(self.loops[1].eval(self.params[1])) < 10

		pyray.draw_circle_lines(pos.x, pos.y, 10, color)

	def get_next_loop(self):
		return self.loops[self.next_loop_id]

	def set_next_loop_id(self):
		dir1 = self.loops[0].derivative(self.params[0])
		dir2 = self.loops[1].derivative(self.params[1])

		det = dir1.x * dir2.y - dir2.x * dir1.y

		if det == 0:
			raise NotImplementedError("Loops are tangential at an intersection point")

		if self.loops[0].turning_number == self.loops[1].turning_number == 1:
			if det > 0:
				self.next_loop_id = 0
			else:
				self.next_loop_id = 1

		elif self.loops[0].turning_number == self.loops[1].turning_number == -1:
			if det > 0:
				self.next_loop_id = 1
			else:
				self.next_loop_id = 0

		else:
			raise NotImplementedError(
				f"Intersecting loops must have the same turning number (1 or -1)."
				f"\n(They were {self.loops[0].turning_number} and {self.loops[1].self.loops[0].turning_number})"
			)

	def __repr__(self):
		return f"LoopIntersection(params: {self.params}, next_loop_id: {self.next_loop_id})"