from math import degrees
import unittest
from util import IntVec
from geometry import Loop

class TestLoop(unittest.TestCase):
	def setUp(self):
		points = [
			(1000, 7500),
			(1000, 7000),
			(1000, 6000),
			(2000, 6000),
			(2000, 6000),
			(5000, 1000),
			(7000, 1500),
			(6000, 2000),
			(8000, 3500),
			(6000, 5000),
			(7000, 6000),
			(9000, 6500),
			(7000, 7000),
			(6000, 8500),
			(8000, 8500),
			(8000, 10000),
			(8000, 11000),
			(7000, 11000),
			(6000, 11000),
			(6000, 12000),
			(6000, 13000),
			(3000, 13000),
			(3000, 12000),
			(5000, 11000),
			(4000, 10500),
			(3000, 11000),
			(2000, 10000),
			(5000, 9000),
			(4000, 7000),
			(2000, 9000),
			(1000, 9000),
			(1000, 8000)
		]

		loop1 = Loop.from_points(points)
		loop2 = Loop.from_points(list(reversed(points[1:] + [points[0]])))

		self.loops = (loop1, loop2)

	def test_is_point_inside_1(self):
		for loop in self.loops:
			for i in range(20):
				for j in range(-10, 10):
					self.assertFalse(loop.is_point_inside(IntVec(j * 100, i * 1000)))
					self.assertFalse(loop.is_point_inside(IntVec(10000 - j * 100, i * 1000)))

	def test_is_point_inside_2(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(1000, 6000)))
			self.assertFalse(loop.is_point_inside(IntVec(999, 8000)))
			self.assertTrue (loop.is_point_inside(IntVec(1001, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(1000, 10000)))

	def test_is_point_inside_3(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(1500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(1500, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(1500, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(1500, 10000)))

	def test_is_point_inside_4(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(2000, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(2000, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(2000, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(2000, 10000)))

	def test_is_point_inside_5(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(2500, 4000)))
			self.assertFalse(loop.is_point_inside(IntVec(2500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(2500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(2500, 7000)))
			self.assertFalse(loop.is_point_inside(IntVec(2500, 9000)))
			self.assertFalse(loop.is_point_inside(IntVec(2500, 10000)))
			self.assertFalse(loop.is_point_inside(IntVec(2500, 11000)))
			self.assertFalse(loop.is_point_inside(IntVec(2500, 12000)))

	def test_is_point_inside_6(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(3000, 4000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(3000, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(3000, 10500)))
			self.assertFalse(loop.is_point_inside(IntVec(3000, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(3000, 14000)))

	def test_is_point_inside_7(self):
		for loop in self.loops:
			self.assertTrue (loop.is_point_inside(IntVec(3500, 4000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(3500, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 10500)))
			self.assertFalse(loop.is_point_inside(IntVec(3500, 11000)))
			self.assertTrue (loop.is_point_inside(IntVec(3500, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(3500, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(3500, 14000)))

	def test_is_point_inside_8(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(4000, 2500)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 3000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(4000, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 10500)))
			self.assertFalse(loop.is_point_inside(IntVec(4000, 11000)))
			self.assertTrue (loop.is_point_inside(IntVec(4000, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(4000, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(4000, 14000)))

	def test_is_point_inside_9(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(5000,  500)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 1500)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 2000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 3000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 8000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(5000, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(5000, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(5000, 14000)))

	def test_is_point_inside_10(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(5500, 1000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 1500)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 2000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 3000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 4000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 8000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 11000)))
			self.assertTrue (loop.is_point_inside(IntVec(5500, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(5500, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(5500, 14000)))

	def test_is_point_inside_11(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(6000, 1000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 1500)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 2500)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 3000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 4000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 4500)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 5500)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 8000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 11000)))
			self.assertTrue (loop.is_point_inside(IntVec(6000, 11500)))
			self.assertFalse(loop.is_point_inside(IntVec(6000, 12500)))
			self.assertFalse(loop.is_point_inside(IntVec(6000, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(6000, 14000)))

	def test_is_point_inside_12(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(6500, 1000)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 1500)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 2000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 2500)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 3000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 3500)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 4000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 4500)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 5500)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 7000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 7500)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 8500)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 10000)))
			self.assertTrue (loop.is_point_inside(IntVec(6500, 11000)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 11500)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(6500, 14000)))

	def test_is_point_inside_13(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(7000, 1000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 1500)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 2000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 2500)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 3000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 4000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 4500)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 5000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 5500)))
			self.assertTrue (loop.is_point_inside(IntVec(7000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(7000, 7000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 7500)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 8500)))
			self.assertTrue (loop.is_point_inside(IntVec(7000, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(7000, 10000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(7000, 14000)))

	def test_is_point_inside_14(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(7500, 1000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 2000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 3000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 4000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 5000)))
			self.assertTrue (loop.is_point_inside(IntVec(7500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(7500, 6500)))
			self.assertTrue (loop.is_point_inside(IntVec(7500, 7000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 7500)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 8500)))
			self.assertTrue (loop.is_point_inside(IntVec(7500, 9000)))
			self.assertTrue (loop.is_point_inside(IntVec(7500, 10000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 11000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(7500, 14000)))

	def test_is_point_inside_15(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(8000, 1000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 2000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 3000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 4000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 5000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(8000, 6500)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 7000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 9000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 11000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(8000, 14000)))

	def test_is_point_inside_16(self):
		for loop in self.loops:
			self.assertFalse(loop.is_point_inside(IntVec(8500, 1000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 2000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 3000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 4000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 5000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 6000)))
			self.assertTrue (loop.is_point_inside(IntVec(8500, 6500)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 7000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 8000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 9000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 11000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 12000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 13000)))
			self.assertFalse(loop.is_point_inside(IntVec(8500, 14000)))

	def test_turning_angle(self):
		self.assertLess(abs(degrees(self.loops[0].calculate_turning_angle()) - 360), 1)
		self.assertLess(abs(degrees(self.loops[1].calculate_turning_angle()) + 360), 1)

	def test_turning_number(self):
		self.assertEqual(self.loops[0].turning_number, 1)
		self.assertEqual(self.loops[1].turning_number, -1)
