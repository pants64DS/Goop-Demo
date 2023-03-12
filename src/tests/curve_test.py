from math import degrees
import unittest
from geometry import make_curve
from util import IntVec, get_angle_between

class TestCurves(unittest.TestCase):
	def setUp(self):
		self.curves = (
			make_curve((3000, 2000), (1000, 4000), (5000, 5000)),
			make_curve((5000, 5000), (1000, 4000), (3000, 2000)),
			make_curve((2000, 4000), (6000, 7000), (7000, 2000)),
			make_curve((7000, 2000), (6000, 7000), (2000, 4000)),
			make_curve((7000, 7000), (1000, 1000), (3000, 5000)),
			make_curve((3000, 5000), (1000, 1000), (7000, 7000)),
			make_curve((1000, 5000), (4000, 1000), (7000, 5000)),
			make_curve((7000, 5000), (4000, 1000), (1000, 5000)),
			make_curve((6000, 7000), (1000, 2000), (6000, 4000)),
			make_curve((6000, 4000), (1000, 2000), (6000, 7000)),
			make_curve((2000, 2000), (2000, 4000), (2000, 6000)),
			make_curve((2000, 9000), (5000,    0), (4000, 3000)),
		)

	def assert_intersections_impl(self, curve1, curve2, correct_points):
		intersections = curve1.find_intersections(curve2)
		self.assertEqual(len(intersections), len(correct_points))

		result_points1 = [i.get_pos(on_curve1=True)  for i in intersections]
		result_points2 = [i.get_pos(on_curve1=False) for i in intersections]

		result_points1.sort(key=lambda v: v.scalars)
		result_points2.sort(key=lambda v: v.scalars)

		for res1, res2, correct_point in zip(result_points1, result_points2, correct_points):
			self.assertLess(res1.dist(IntVec(correct_point)), 1)
			self.assertLess(res2.dist(IntVec(correct_point)), 1)

	def assert_intersections(self, curve1, curve2, *correct_points):
		correct_points = sorted(correct_points)
		self.assert_intersections_impl(curve1, curve2, correct_points)
		self.assert_intersections_impl(curve2, curve1, correct_points)

	def test_get_coeff_vectors(self):
		c, b, a = make_curve((4, 3), (2, 1), (3, 5)).get_coeff_vectors()

		self.assertEqual(a, IntVec(3, 6))
		self.assertEqual(b, IntVec(-4, -4))
		self.assertEqual(c, IntVec(4, 3))

	def test_get_x_coeffs(self):
		c, b, a = make_curve((4, 3), (2, 1), (3, 5)).get_x_coeffs()

		self.assertEqual(a, 3)
		self.assertEqual(b, -4)
		self.assertEqual(c, 4)

	def test_get_y_coeffs(self):
		c, b, a = make_curve((4, 3), (2, 1), (3, 5)).get_y_coeffs()

		self.assertEqual(a, 6)
		self.assertEqual(b, -4)
		self.assertEqual(c, 3)

	def test_eval_xy(self):
		for curve in self.curves:
			for i in range(17):
				t = i / 16
				self.assertEqual(curve.eval(t), (curve.eval_x(t), curve.eval_y(t)))

	def test_different_axes_no_intersections(self):
		curve1 = make_curve((4000, 8000), (4500, 5000), (1000, 6000))
		curve2 = make_curve((1000, 3000), (4000, 9000), (6000, 2000))

		self.assert_intersections(curve1, curve2)

	def test_different_axes_one_intersection_1(self):
		curve1 = make_curve((2000, 7000), (4000, 3000), (6000, 7000))
		curve2 = make_curve((7000, 2000), (1000, 5000), (7000, 8000))

		self.assert_intersections(curve1, curve2, (4000, 5000))

	def test_different_axes_one_intersection_2(self):
		curve1 = make_curve((1000, 4000), (8000, 11000), (7000, 4000))
		curve2 = make_curve((8000, 5000), (2000, 10000), (7000, 3000))

		self.assert_intersections(curve1, curve2, (7122, 5714))

	def test_different_axes_two_intersections_1(self):
		curve1 = make_curve((2000, 5000), (5000, 10000), (8000, 5000))
		curve2 = make_curve((3000, 8000), (3000,  4000), (9000, 7000))

		self.assert_intersections(curve1, curve2, (3253, 6652), (7168, 6195))

	def test_different_axes_two_intersections_2(self):
		curve1 = make_curve((1000, 6000), (4000, 5000), (2000, 3000))
		curve2 = make_curve((4000, 8000), (1000, 3000), (5000, 4000))

		self.assert_intersections(curve1, curve2, (2714, 4842), (2797, 4360))

	def test_different_axes_two_intersections_3(self):
		curve1 = make_curve((1000, 5500), (8500, 4500), (1000, 3000))
		curve2 = make_curve((1000, 7000), (1500, 1000), (3000, 3000))

		self.assert_intersections(curve1, curve2, (1159, 5478), (1684, 3143))

	def test_different_axes_three_intersections_1(self):
		curve1 = make_curve((1000, 4000), (8000, 3000), (3000, 2000))
		curve2 = make_curve((2000, 1000), (3000, 9000), (4000,    0))

		self.assert_intersections(curve1, curve2, (2457, 3769), (3472, 3566), (3724, 2160))

	def test_different_axes_three_intersections_2(self):
		curve1 = make_curve((9000,  11000), (6000, 11000), (9000, 6000))
		curve2 = make_curve((10000, 12000), (5000,  9000), (9000, 7000))

		self.assert_intersections(curve1, curve2, (7504,  9871), (8190, 7480), (8498, 10957))

	def test_different_axes_four_intersections_1(self):
		curve1 = make_curve((1000, 5000), (15000, 3000), (1000, 1000))
		curve2 = make_curve((7000, 1000), (5000, 10000), (3000,    0))

		self.assert_intersections(curve1, curve2, (3292, 1360), (4282, 4458), (6122, 4036), (6725, 2147))

	def test_different_axes_four_intersections_2(self):
		curve1 = make_curve((2000, 4000), (9000, 1000), (1000, 7000))
		curve2 = make_curve((1000, 3000), (9000, 9000), (1000, 2000))

		self.assert_intersections(curve1, curve2, (2219, 3907), (2858, 3644), (3633, 4932), (3961, 4651))

	def test_vertical_axes_no_intersections_1(self):
		curve1 = make_curve((1000, 1000), (3000, 4000), (5000, 2000))
		curve2 = make_curve((3000, 5000), (2000,    0), (1000, 6000))

		self.assert_intersections(curve1, curve2)

	def test_vertical_axes_no_intersections_2(self):
		curve1 = make_curve((3000, 4000), (4000, 2000), (5000, 4000))
		curve2 = make_curve((7000, 4000), (4000, 5000), (1000, 4000))

		self.assert_intersections(curve1, curve2)

	def test_vertical_axes_one_intersection_1(self):
		curve1 = make_curve((1000, 4000), (2000, 2000), (3000, 5000))
		curve2 = make_curve((4000, 6000), (3000, 3000), (2000, 5000))

		self.assert_intersections(curve1, curve2, (2700, 4212))

	def test_vertical_axes_one_intersection_2(self):
		curve1 = make_curve((1000, 3000), (2000, 2000), (3000, 3000))
		curve2 = make_curve((2000, 1000), (3000, 5000), (4000, 2000))

		self.assert_intersections(curve1, curve2, (2538, 2644))

	def test_vertical_axes_two_intersections_1(self):
		curve1 = make_curve((5000, 4000), (3000, 3000), (1000, 6000))
		curve2 = make_curve((4000, 5000), (3000, 1000), (2000, 7000))

		self.assert_intersections(curve1, curve2, (2626, 4222), (3595, 3791))

	def test_vertical_axes_two_intersections_2(self):
		curve1 = make_curve((5000, 1000), (3500, 3500), (2000, 2500))
		curve2 = make_curve((5000, 2500), (4000, 1000), (3000, 3500))

		self.assert_intersections(curve1, curve2, (3391, 2675), (4329, 1944))

	def test_parallel_axes_no_intersections_1(self):
		curve1 = make_curve((2500, 2500), (3000, 1000), (4500, 1500))
		curve2 = make_curve((1000, 2000), (2500, 2500), (3000, 1000))

		self.assert_intersections(curve1, curve2)

	def test_parallel_axes_no_intersections_2(self):
		curve1 = make_curve((2500, 2000), (4000, 2500), (4500, 1000))
		curve2 = make_curve((1000, 2000), (2500, 2500), (3000, 1000))

		self.assert_intersections(curve1, curve2)

	def test_parallel_axes_one_intersection_1(self):
		curve1 = make_curve((3500, 3500), (1000, 1000), (4500, 1500))
		curve2 = make_curve((2000, 4000), (1500, 2500), (3000, 2000))

		self.assert_intersections(curve1, curve2, (2518, 2217))

	def test_parallel_axes_one_intersection_2(self):
		curve1 = make_curve((2000, 2500), (3000, 3500), (1500, 4500))
		curve2 = make_curve((1000, 2500), (2500, 4000), (1000, 5500))

		self.assert_intersections(curve1, curve2, (1709, 4352))

	def test_parallel_axes_two_intersections_1(self):
		curve1 = make_curve((1000, 2500), (3500, 2500), (3500, 5000))
		curve2 = make_curve((1500, 3000), (4000, 1500), (2500, 4000))

		self.assert_intersections(curve1, curve2, (2113, 2663), (2930, 3183))

	def test_parallel_axes_two_intersections_2(self):
		curve1 = make_curve((2000, 2500), (2500, 1000), (4000, 1500))
		curve2 = make_curve((3000, 1000), (2500, 2500), (1000, 2000))

		self.assert_intersections(curve1, curve2, (2218, 2015), (2782, 1485))

	def test_one_linear_curve_no_intersections_1(self):
		curve1 = make_curve((3000, 1000), (5000, 3000), (7000, 5000))
		curve2 = make_curve((2000, 2000), (5000, 2000), (5000, 5000))

		self.assert_intersections(curve1, curve2)

	def test_one_linear_curve_no_intersections_2(self):
		curve1 = make_curve((6000, 1000), (5000, 3000), (3000, 7000))
		curve2 = make_curve((4000, 4000), (1000, 1000), (3000, 5000))

		self.assert_intersections(curve1, curve2)

	def test_one_linear_curve_no_intersections_3(self):
		curve1 = make_curve((1000, 1000), (2000, 3000), (3000, 5000))
		curve2 = make_curve((4000, 4000), (5000, 1000), (8000, 2000))

		self.assert_intersections(curve1, curve2)

	def test_one_linear_curve_no_intersections_4(self):
		curve1 = make_curve((7000, 4000), (7000, 7000), (4000, 7000))
		curve2 = make_curve((4000, 3000), (2000, 1000), (6000, 5000))

		self.assert_intersections(curve1, curve2)

	def test_one_linear_curve_one_intersection_1(self):
		curve1 = make_curve((1000, 4000), (4000, 3000), (5000, 6000))
		curve2 = make_curve((5000, 3000), (6000, 1000), (3000, 7000))

		self.assert_intersections(curve1, curve2, (4220, 4560))

	def test_one_linear_curve_one_intersection_2(self):
		curve1 = make_curve((1000, 2000), (2000, 6000), (7000, 5000))
		curve2 = make_curve((2000, 3000), (5000, 5000), (8000, 7000))

		self.assert_intersections(curve1, curve2, (5298, 5199))

	def test_one_linear_curve_two_intersections_1(self):
		curve1 = make_curve((5000, 4000), (9000, 6000), (2000, 5000))
		curve2 = make_curve((7000, 3000), (4000, 5000), (1000, 7000))

		self.assert_intersections(curve1, curve2, (3679, 5214), (5283, 4145))

	def test_one_linear_curve_two_intersections_2(self):
		curve1 = make_curve((8000, 4000), (4000, 4000), (2000, 4000))
		curve2 = make_curve((7000, 3000), (5000, 9000), (3000, 2000))

		self.assert_intersections(curve1, curve2, (3678, 4000), (6630, 4000))

	def test_one_vertical_linear_curve_no_intersections_1(self):
		curve1 = make_curve((3000, 6000), (3000, 5000), (3000, 1000))
		curve2 = make_curve((4000, 5000), (2000, 1000), (6000, 3000))

		self.assert_intersections(curve1, curve2)

	def test_one_vertical_linear_curve_no_intersections_2(self):
		curve1 = make_curve((2000, 4000), (3000, 1000), (4000, 6000))
		curve2 = make_curve((5000, 5000), (5000, 1000), (5000, 3000))

		self.assert_intersections(curve1, curve2)

	def test_one_vertical_linear_curve_one_intersection_1(self):
		curve1 = make_curve((3000, 4000), (1000, 2000), (5000, 3000))
		curve2 = make_curve((4000, 5000), (4000, 4000), (4000, 2000))

		self.assert_intersections(curve1, curve2, (4000, 2779))

	def test_one_vertical_linear_curve_one_intersection_2(self):
		curve1 = make_curve((3000, 6000), (3000, 3000), (3000, 2000))
		curve2 = make_curve((1000, 2000), (3000, 1000), (5000, 5000))

		self.assert_intersections(curve1, curve2, (3000, 2250))

	def test_one_vertical_linear_curve_two_intersections_1(self):
		curve1 = make_curve((2000, 5000), (6000, 3000), (1000, 1000))
		curve2 = make_curve((3000, 1000), (3000, 3000), (3000, 5000))

		self.assert_intersections(curve1, curve2, (3000, 4398), (3000, 2046))

	def test_one_vertical_linear_curve_two_intersections_2(self):
		curve1 = make_curve((5000, 3000), (1000, 1000), (8000, 8000))
		curve2 = make_curve((4000, 2000), (4000, 2000), (4000, 5000))

		self.assert_intersections(curve1, curve2, (4000, 3625), (4000, 2590))

	def test_two_linear_curves_no_intersections_1(self):
		curve1 = make_curve((2500, 1500), (2000, 1000), (1500,  500))
		curve2 = make_curve((2000, 1500), (1500, 2000), (1000, 2500))

		self.assert_intersections(curve1, curve2)

	def test_two_linear_curves_no_intersections_2(self):
		curve1 = make_curve((4000, 4000), (3000, 2000), (5000, 6000))
		curve2 = make_curve((2000, 5000), (1000, 3000), (4000, 9000))

		self.assert_intersections(curve1, curve2)

	def test_two_linear_curves_one_intersection_1(self):
		curve1 = make_curve((5000, 8000), (3000, 5000), (1000, 2000))
		curve2 = make_curve((5000, 5000), (8000, 1000), (2000, 9000))

		self.assert_intersections(curve1, curve2, (3941, 6412))

	def test_two_linear_curves_one_intersection_2(self):
		curve1 = make_curve((1000, 2000), (3000, 2000), (5000, 2000))
		curve2 = make_curve((4000, 1000), (4000, 3000), (4000, 4000))

		self.assert_intersections(curve1, curve2, (4000, 2000))

	def test_one_singular_curve_no_intersections_1(self):
		curve1 = make_curve((4000, 3000), (3000, 2000), (2000, 3000))
		curve2 = make_curve((3000, 3000), (3000, 3000), (3000, 3000))

		self.assert_intersections(curve1, curve2)

	def test_one_singular_curve_no_intersections_2(self):
		curve1 = make_curve((4000, 4000), (3000, 2000), (2000, 4000))
		curve2 = make_curve((3000, 3000), (3000, 3000), (3000, 3000))

		self.assert_intersections(curve1, curve2)

	def test_clip_until(self):
		for og_curve in self.curves:
			for i in range(17):
				t = i / 16
				clipped_curve = og_curve.clip_until(t)

				self.assertLess(clipped_curve.p0.dist(og_curve.eval(t)), 1.5)
				self.assertEqual(clipped_curve.p2, og_curve.p2)

				if clipped_curve.p0 == clipped_curve.p2:
					continue

				angle1 = get_angle_between(og_curve.derivative(t), clipped_curve.derivative(0))
				angle2 = get_angle_between(og_curve.derivative(1), clipped_curve.derivative(1))

				self.assertLess(degrees(angle1), 1)
				self.assertLess(degrees(angle2), 1)

	def test_clip_after(self):
		for og_curve in self.curves:
			for i in range(17):
				t = i / 16
				clipped_curve = og_curve.clip_after(t)

				self.assertLess(clipped_curve.p2.dist(og_curve.eval(t)), 1.5)
				self.assertEqual(clipped_curve.p0, og_curve.p0)

				if clipped_curve.p0 == clipped_curve.p2:
					continue

				angle1 = get_angle_between(og_curve.derivative(t), clipped_curve.derivative(1))
				angle2 = get_angle_between(og_curve.derivative(0), clipped_curve.derivative(0))

				self.assertLess(degrees(angle1), 1)
				self.assertLess(degrees(angle2), 1)

	def test_clip_after_until(self):
		for og_curve in self.curves:
			for i in range(17):
				for j in range(i, 17):
					t1 = i / 16
					t2 = j / 16
					clipped_curve = og_curve.clip_after_until(t1, t2)

					self.assertLess(clipped_curve.p0.dist(og_curve.eval(t1)), 1.5)
					self.assertLess(clipped_curve.p2.dist(og_curve.eval(t2)), 1.5)

					if clipped_curve.p0 == clipped_curve.p2:
						continue

					angle1 = get_angle_between(og_curve.derivative(t1), clipped_curve.derivative(0))
					angle2 = get_angle_between(og_curve.derivative(t2), clipped_curve.derivative(1))

					self.assertLess(degrees(angle1), 1)
					self.assertLess(degrees(angle2), 1)
