import unittest
from geometry import ParabolicCurve
from util import IntVec2

class TestParabolicCurve(unittest.TestCase):
	def setUp(self):
		self.curve = ParabolicCurve((11, 12), (13, 14), (15, 16))

	def test_get_coeff_vectors(self):
		c, b, a = self.curve.get_coeff_vectors()
		self.assertEqual(a, IntVec2(0, 0))
		self.assertEqual(b, IntVec2(4, 4))
		self.assertEqual(c, IntVec2(11, 12))

	def test_get_x_coeffs(self):
		c, b, a = self.curve.get_x_coeffs()
		self.assertEqual(a, 0)
		self.assertEqual(b, 4)
		self.assertEqual(c, 11)

	def test_get_y_coeffs(self):
		c, b, a = self.curve.get_y_coeffs()
		self.assertEqual(a, 0)
		self.assertEqual(b, 4)
		self.assertEqual(c, 12)

	def test_one_intersection(self):
		curve1 = ParabolicCurve((2000, 7000), (4000, 3000), (6000, 7000))
		curve2 = ParabolicCurve((7000, 2000), (1000, 5000), (7000, 8000))
		tolerance = 1

		intersections = curve1.find_intersections(curve2)
		points = [i.get_pos() for i in intersections]

		self.assertEqual(len(points), 1)
		self.assertLessEqual(points[0].dist(IntVec2(4000, 5000)), tolerance)

		intersections = curve2.find_intersections(curve1)
		points = [i.get_pos() for i in intersections]

		self.assertEqual(len(points), 1)
		self.assertLessEqual(points[0].dist(IntVec2(4000, 5000)), tolerance)

	def test_two_intersections(self):
		curve1 = ParabolicCurve((2000, 5000), (5000, 10000), (8000, 5000))
		curve2 = ParabolicCurve((3000, 8000), (3000,  4000), (9000, 7000))
		tolerance = 1

		intersections = curve1.find_intersections(curve2)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 2)
		self.assertLessEqual(points[0].dist(IntVec2(3253, 6652)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(7168, 6195)), tolerance)

		intersections = curve2.find_intersections(curve1)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 2)
		self.assertLessEqual(points[0].dist(IntVec2(3253, 6652)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(7168, 6195)), tolerance)

	def test_three_intersections(self):
		curve1 = ParabolicCurve((9000,  11000), (6000, 11000), (9000, 6000))
		curve2 = ParabolicCurve((10000, 12000), (5000,  9000), (9000, 7000))
		tolerance = 1

		intersections = curve1.find_intersections(curve2)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 3)
		self.assertLessEqual(points[0].dist(IntVec2(7504,  9871)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(8190,  7480)), tolerance)
		self.assertLessEqual(points[2].dist(IntVec2(8498, 10957)), tolerance)

		intersections = curve2.find_intersections(curve1)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 3)
		self.assertLessEqual(points[0].dist(IntVec2(7504,  9871)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(8190,  7480)), tolerance)
		self.assertLessEqual(points[2].dist(IntVec2(8498, 10957)), tolerance)

	def test_four_intersections(self):
		curve1 = ParabolicCurve((1000, 5000), (15000, 3000), (1000, 1000))
		curve2 = ParabolicCurve((7000, 1000), (5000, 10000), (3000,    0))
		tolerance = 1.5

		intersections = curve1.find_intersections(curve2)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 4)
		self.assertLessEqual(points[0].dist(IntVec2(3292, 1360)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(4282, 4458)), tolerance)
		self.assertLessEqual(points[2].dist(IntVec2(6122, 4036)), tolerance)
		self.assertLessEqual(points[3].dist(IntVec2(6725, 2147)), tolerance)

		intersections = curve2.find_intersections(curve1)
		points = sorted([i.get_pos() for i in intersections], key=lambda v: v.x)

		self.assertEqual(len(points), 4)
		self.assertLessEqual(points[0].dist(IntVec2(3292, 1360)), tolerance)
		self.assertLessEqual(points[1].dist(IntVec2(4282, 4458)), tolerance)
		self.assertLessEqual(points[2].dist(IntVec2(6122, 4036)), tolerance)
		self.assertLessEqual(points[3].dist(IntVec2(6725, 2147)), tolerance)
