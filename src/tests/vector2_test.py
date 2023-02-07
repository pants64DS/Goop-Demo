import unittest
from math import sqrt
from util.vector2 import IntVec2

class TestIntVec2(unittest.TestCase):
	def setUp(self):
		self.a = IntVec2(1, 2)
		self.b = IntVec2(3, 4)

	def test_get_x(self):
		self.assertEqual(self.a.x, 1)
		self.assertEqual(self.b.x, 3)

	def test_get_y(self):
		self.assertEqual(self.a.y, 2)
		self.assertEqual(self.b.y, 4)

	def test_set_x(self):
		self.a.x = -11
		self.b.x = -12

		self.assertEqual(self.a.x, -11)
		self.assertEqual(self.b.x, -12)

	def test_set_y(self):
		self.a.y = -13
		self.b.y = -14

		self.assertEqual(self.a.y, -13)
		self.assertEqual(self.b.y, -14)

	def test_subscript(self):
		self.assertEqual(self.a[0], 1)
		self.assertEqual(self.a[1], 2)
		self.assertEqual(self.b[0], 3)
		self.assertEqual(self.b[1], 4)

	def test_add(self):
		self.assertEqual(self.a + self.b, IntVec2(4, 6))
		self.assertEqual(self.b + self.a, IntVec2(4, 6))

	def test_sub(self):
		self.assertEqual(self.a - self.b, IntVec2(-2, -2))
		self.assertEqual(self.b - self.a, IntVec2( 2,  2))

	def test_mul(self):
		self.assertEqual(self.a  * 3, IntVec2(3, 6))
		self.assertEqual(self.b * -5, IntVec2(-15, -20))

	def test_rmul(self):
		self.assertEqual(3  * self.a, IntVec2(3, 6))
		self.assertEqual(-5 * self.b, IntVec2(-15, -20))

	def test_neg(self):
		self.assertEqual(-self.a, IntVec2(-1, -2))
		self.assertEqual(-self.b, IntVec2(-3, -4))

	def test_eq(self):
		self.assertTrue(self.a == self.a)
		self.assertTrue(self.b == self.b)
		self.assertTrue(self.a == IntVec2(self.a))
		self.assertTrue(self.b == IntVec2(self.b))
		self.assertTrue(self.a != self.b)
		self.assertTrue(self.b != self.a)

	def test_str(self):
		self.assertEqual(str(self.a), '(1, 2)')
		self.assertEqual(str(self.b), '(3, 4)')

	def test_repr(self):
		self.assertEqual(repr(self.a), 'IntVec2(1, 2)')
		self.assertEqual(repr(self.b), 'IntVec2(3, 4)')

	def test_length(self):
		self.assertAlmostEqual(self.a.length(), sqrt(5))
		self.assertAlmostEqual(self.b.length(), 5)

	def test_dist(self):
		self.assertAlmostEqual(self.a.dist(self.b), sqrt(8))
		self.assertAlmostEqual(self.b.dist(self.a), sqrt(8))
