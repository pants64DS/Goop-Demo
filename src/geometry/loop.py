from math import floor, ceil
import pyray
from numpy import sign
from util import IntVec, get_angle_between
from geometry import make_curve

def next_cyclic_element(l, i):
	i += 1
	if i < len(l):
		return l[i]
	return l[0]

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

	def sanitize(self):
		if not self.curves:
			return False

		self.curves = [curve for curve in self.curves if curve.p0 != curve.p2]

		for i in range(len(self.curves) - 1):
			self.curves[i] = self.curves[i].change_endpoint(self.curves[i + 1].p0)

		self.curves[-1] = self.curves[-1].change_endpoint(self.curves[0].p0)
		return True

	def get_curve(self, t):
		return self.curves[floor(t) % len(self.curves)]

	def eval(self, t):
		return self.get_curve(t).eval(t % 1)

	def derivative(self, t):
		return self.get_curve(t).derivative(t % 1)

	def second_derivative(self, t):
		return self.get_curve(t).second_derivative()

	@classmethod
	def from_points(cls, points):
		if len(points) & 1:
			raise ValueError("The number of points must be even")

		curves = []
		for i in range(1, len(points) - 1, 2):
			curves.append(make_curve(points[i], points[i + 1], points[i + 2]))

		curves.append(make_curve(points[-1], points[0], points[1]))

		return cls(curves)

	def draw(self, color, thickness=2): # pragma: no cover
		for curve in self.curves:
			curve.draw(color, thickness)

	def draw_lines(self): # pragma: no cover
		for curve in self.curves:
			curve.draw_lines(pyray.RED)

	# Assumes that the loop doesn't intersect itself
	def is_point_inside(self, point):
		line_x = point.x
		line_start_y = point.y
		parity = 0

		for curve in self.curves:
			bbox = curve.get_bounding_box()

			if bbox.top_y <= line_start_y:
				parity += curve.parity_of_vertical_line_intersections(line_x)

			elif bbox.left_x <= line_x <= bbox.right_x and bbox.bottom_y <= line_start_y:
				for t in curve.find_vertical_line_intersections(line_x):
					if curve.eval_y(t) <= line_start_y:
						parity += 1

			if line_x == curve.p0.x \
			and line_start_y > curve.p0.y \
			and curve.starts_going_left():
				parity += 1

			if line_x == curve.p2.x \
			and line_start_y > curve.p2.y \
			and curve.ends_going_left():
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
			side_vectors += curve.get_side_vectors()

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

		return results

	def get_intersections(self, other_loops):
		intersections_by_loop = []
		all_intersections = []

		for other in other_loops:
			new_intersections = Loop.get_intersections_between(self, other)
			all_intersections += new_intersections

			new_intersections.sort(key=lambda intersection: intersection.params[1])
			intersections_by_loop.append(new_intersections)

		all_intersections.sort(key=lambda intersection: intersection.params[0])

		for i in range(len(all_intersections)):
			if all_intersections[i].get_next_preferred_loop() is self:
				all_intersections[i].next_preferred_intersection \
					= next_cyclic_element(all_intersections, i)

			if all_intersections[i].get_next_alternative_loop() is self:
				all_intersections[i].next_alternative_intersection \
					= next_cyclic_element(all_intersections, i)

		for loop, intersections in zip(other_loops, intersections_by_loop):
			for i in range(len(intersections)):
				if intersections[i].get_next_preferred_loop() is loop:
					intersections[i].next_preferred_intersection \
						= next_cyclic_element(intersections, i)

				if intersections[i].get_next_alternative_loop() is loop:
					intersections[i].next_alternative_intersection \
						= next_cyclic_element(intersections, i)

		return all_intersections

	@staticmethod
	def trace_intersections(results, curr_node):
		if results and curr_node == results[0]:
			return True

		# If already visited
		if curr_node.followed_loop_id is not None:
			raise RuntimeError("Intersection already visited when creating a loop")
			# return False

		results.append(curr_node)
		num_results = len(results)

		curr_node.followed_loop_id = curr_node.next_preferred_loop_id

		if Loop.trace_intersections(results, curr_node.next_preferred_intersection):
			return True

		curr_node.followed_loop_id = int(not curr_node.next_preferred_loop_id)

		return Loop.trace_intersections(results[:num_results], \
			curr_node.next_alternative_intersection)

	def merge_to(self, loops):
		if not loops:
			return self, []

		intersections = self.get_intersections(loops)

		results = []

		for start_intersection in intersections:
			if start_intersection.followed_loop_id is not None:
				continue

			new_intersections = []
			Loop.trace_intersections(new_intersections, start_intersection)

			new_loop = Loop([], 0)
			for intersection in new_intersections:
				interval = intersection.get_followed_interval()
				new_loop.curves += intersection.get_followed_loop().clip_interval(*interval)

			if not new_loop.sanitize():
				continue

			new_loop.turning_number = new_loop.calculate_turning_number()

			if new_loop.turning_number == self.turning_number:
				bounding_loop = new_loop

			results.append(new_loop)

		return bounding_loop, [loop for loop in results if loop is not bounding_loop]

	def clip_interval(self, start, end):
		if start == end:
			return []

		start_curve_id = floor(start) % len(self.curves)
		end_curve_id = floor(end) % len(self.curves)

		t1 = start % 1
		t2 = end % 1

		if start_curve_id == end_curve_id and t1 < t2:
			return [self.curves[start_curve_id].clip_after_until(t1, t2)]

		new_curves = [self.curves[start_curve_id].clip_until(t1)]

		curve_id = (start_curve_id + 1) % len(self.curves)
		while curve_id != end_curve_id:
			new_curves.append(self.curves[curve_id])
			curve_id = (curve_id + 1) % len(self.curves)

		new_curves.append(self.curves[end_curve_id].clip_after(t2))

		return new_curves

class LoopIntersection:
	def __init__(self, curve_intersection, loop1, loop2, curve1_id, curve2_id):
		self.params = (curve1_id + curve_intersection.t1, curve2_id + curve_intersection.t2)
		self.loops = (loop1, loop2)

		self.set_next_loop_id()
		self.next_preferred_intersection = None
		self.next_alternative_intersection = None
		self.followed_loop_id = None

	def draw(self, color): # pragma: no cover
		pos = self.loops[0].eval(self.params[0])
		assert pos.dist(self.loops[1].eval(self.params[1])) < 10

		pyray.draw_circle_lines(*IntVec(pos), 10, color)

	def get_next_preferred_loop(self):
		return self.loops[self.next_preferred_loop_id]

	def get_next_alternative_loop(self):
		return self.loops[not self.next_preferred_loop_id]

	def get_followed_loop(self):
		return self.loops[self.followed_loop_id]

	def get_followed_intersection(self):
		return (self.next_preferred_intersection, \
			self.next_alternative_intersection)[self.followed_loop_id != self.next_preferred_loop_id]

	def get_followed_interval(self):
		start = self.params[self.followed_loop_id]
		end = self.get_followed_intersection().params[self.followed_loop_id]

		return start, end

	def get_next_preferred_interval(self):
		start = self.params[self.next_preferred_loop_id]
		end = self.next_preferred_intersection.params[self.next_preferred_loop_id]

		return start, end

	def set_next_loop_id(self):
		dir1 = self.loops[0].derivative(self.params[0])
		dir2 = self.loops[1].derivative(self.params[1])

		x1y2 = dir1.x * dir2.y
		x2y1 = dir2.x * dir1.y

		if x1y2 == x2y1:
			raise NotImplementedError("Loops are tangential at an intersection point")

		if self.loops[0].turning_number == self.loops[1].turning_number == 1:
			if x1y2 > x2y1:
				self.next_preferred_loop_id = 0
			else:
				self.next_preferred_loop_id = 1

		elif self.loops[0].turning_number == self.loops[1].turning_number == -1:
			if x1y2 > x2y1:
				self.next_preferred_loop_id = 1
			else:
				self.next_preferred_loop_id = 0

		else:
			raise NotImplementedError(
				f"Intersecting loops must have the same turning number (1 or -1)."
				f"\n(They were {self.loops[0].turning_number} and {self.loops[1].turning_number})"
			)
