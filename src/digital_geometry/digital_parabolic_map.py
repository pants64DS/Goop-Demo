from itertools import cycle, islice
from collections import Counter
from util import IntVec
from curve import Curve

class NewLoop:
	def __init__(self, curves, color):
		self.curves = curves
		self.color = color # The color on the left side of each curve

		self.assert_valid()

	def assert_valid(self):
		assert len(self.curves) >= 2

		for curve1, curve2 in zip(self.curves, islice(cycle(self.curves), 1, None)):
			assert curve1.p2 == curve2.p0

		startpoints = Counter()
		endpoints   = Counter()
		otherpoints = Counter()

		for curve in self.curves:
			assert curve.p0 != curve.p2

			for point in curve:
				if point == curve.p0:
					startpoints.update([point])
				elif point == curve.p2:
					endpoints.update([point])
				else:
					otherpoints.update([point])

		for startpoint, count in startpoints:
			assert count == 1
			assert endpoints[startpoint] == 1
			assert startpoint not in otherpoints

		for endpoint, count in endpoints:
			assert count == 1
			assert startpoints[endpoint] == 1
			assert endpoint not in otherpoints

		for otherpoint, count in otherpoints:
			assert count == 1
			assert otherpoint not in startpoints
			assert otherpoint not in endpoints

		# TODO: Make sure the loop is counterclockwise

class Edge:
	def __init__(self, curve, start, end, left_color, right_color, next_edges, prev_edges):
		self.curve = curve
		self.left_color = left_color
		self.right_color = right_color
		self.endpoints = [start, end]
		self.next_edges = next_edges
		self.prev_edges = prev_edges

		self.assert_valid()

	def assert_valid(self):
		assert len(self.endpoints) == 2
		assert self.endpoints[0] != self.endpoints[1]
		assert self.endpoints[0] in self.curve
		assert self.endpoints[1] in self.curve

		assert len(self.next_edges) == 3
		assert len(self.prev_edges) == 3

		assert self.left_color != self.right_color

		color = self.right_color

		for i in 0, 1:
			for edge in (self.prev_edges, self.next_edges)[i]:
				if edge is None: continue

				if edge.endpoints[0] == self.endpoints[i]:
					assert edge.left_color == color
					color = edge.right_color

				elif edge.endpoints[1] == self.endpoints[i]:
					assert edge.right_color == color
					color = edge.left_color

				else:
					assert False

			assert color == (self.left_color, self.right_color)[i]

class DigitalParabolicMap:
	def __init__(self):
		self.edges = []

	def add_loop(self, new_loop):
		pass # todo
