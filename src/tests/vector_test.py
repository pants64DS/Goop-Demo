import unittest
import pyray
from math import sqrt
from util import IntVec, FloatVec

class TestIntVec(unittest.TestCase):
	def setUp(self):
		self.a = IntVec(1, 2)
		self.b = IntVec(3, 4)
		self.c = FloatVec(1.125, 2.25)
		self.d = FloatVec(3.5, 5.0)

	def test_get_x(self):
		self.assertEqual(self.a.x, 1)
		self.assertEqual(self.b.x, 3)
		self.assertEqual(self.c.x, 1.125)
		self.assertEqual(self.d.x, 3.5)

	def test_get_y(self):
		self.assertEqual(self.a.y, 2)
		self.assertEqual(self.b.y, 4)
		self.assertEqual(self.c.y, 2.25)
		self.assertEqual(self.d.y, 5.0)

	def test_set_x(self):
		self.a.x = -11
		self.b.x = -12
		self.c.x = -13
		self.d.x = -14

		self.assertEqual(self.a.x, -11)
		self.assertEqual(self.b.x, -12)
		self.assertEqual(self.c.x, -13)
		self.assertEqual(self.d.x, -14)

	def test_set_y(self):
		self.a.y = -15
		self.b.y = -16
		self.c.y = -17
		self.d.y = -18

		self.assertEqual(self.a.y, -15)
		self.assertEqual(self.b.y, -16)
		self.assertEqual(self.c.y, -17)
		self.assertEqual(self.d.y, -18)

	def test_subscript(self):
		self.assertEqual(self.a[0], 1)
		self.assertEqual(self.a[1], 2)
		self.assertEqual(self.b[0], 3)
		self.assertEqual(self.b[1], 4)
		self.assertEqual(self.c[0], 1.125)
		self.assertEqual(self.c[1], 2.25)
		self.assertEqual(self.d[0], 3.5)
		self.assertEqual(self.d[1], 5.0)

	def test_add(self):
		self.assertEqual(self.a + self.b, IntVec(4, 6))
		self.assertEqual(self.c + self.d, FloatVec(4.625, 7.25))
		self.assertEqual(self.a + self.c, FloatVec(2.125, 4.25))
		self.assertEqual(self.a + (0.5, 0.25), (1.5, 2.25))
		self.assertEqual(self.b + (1, -1), (4, 3))

	def test_sub(self):
		self.assertEqual(self.a - self.b, IntVec(-2, -2))
		self.assertEqual(self.b - self.a, IntVec( 2,  2))

	def test_mul(self):
		self.assertEqual(self.a  * 3, IntVec(3, 6))
		self.assertEqual(self.b * -5, IntVec(-15, -20))

	def test_rmul(self):
		self.assertEqual(3  * self.a, IntVec(3, 6))
		self.assertEqual(-5 * self.b, IntVec(-15, -20))

	def test_floordiv(self):
		self.assertEqual(self.a // 2, IntVec(0, 1))
		self.assertEqual(self.b // 3, IntVec(1, 1))

	def test_truediv(self):
		self.assertEqual(self.a / 2, FloatVec(0.5, 1))
		self.assertEqual(self.b / 4, FloatVec(0.75, 1))

	def test_neg(self):
		self.assertEqual(-self.a, IntVec(-1, -2))
		self.assertEqual(-self.b, IntVec(-3, -4))

	def test_eq(self):
		self.assertTrue(self.a == self.a)
		self.assertTrue(self.b == self.b)
		self.assertTrue(self.a == IntVec(self.a))
		self.assertTrue(self.b == IntVec(self.b))
		self.assertTrue(self.a != self.b)
		self.assertTrue(self.b != self.a)

	def test_str(self):
		self.assertEqual(str(self.a), '(1, 2)')
		self.assertEqual(str(self.b), '(3, 4)')
		self.assertEqual(str(self.c), '(1.125, 2.25)')
		self.assertEqual(str(self.d), '(3.5, 5.0)')

	def test_repr(self):
		self.assertEqual(repr(self.a), 'IntVec(1, 2)')
		self.assertEqual(repr(self.b), 'IntVec(3, 4)')
		self.assertEqual(repr(self.c), 'FloatVec(1.125, 2.25)')
		self.assertEqual(repr(self.d), 'FloatVec(3.5, 5.0)')

	def test_length(self):
		self.assertAlmostEqual(self.a.length(), sqrt(5))
		self.assertAlmostEqual(self.b.length(), 5)

	def test_dist(self):
		self.assertAlmostEqual(self.a.dist(self.b), sqrt(8))
		self.assertAlmostEqual(self.b.dist(self.a), sqrt(8))

	def test_to_pyray_vector2(self):
		a = self.a.to_pyray_vector2()
		b = self.b.to_pyray_vector2()

		self.assertEqual(a.x, self.a.x)
		self.assertEqual(a.y, self.a.y)
		self.assertEqual(b.x, self.b.x)
		self.assertEqual(b.y, self.b.y)

	def test_from_pyray_vector2(self):
		self.assertEqual(IntVec.from_pyray_vector2(pyray.Vector2(1, 2)), self.a)
		self.assertEqual(IntVec.from_pyray_vector2(pyray.Vector2(3, 4)), self.b)
