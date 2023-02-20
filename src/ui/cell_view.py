from math import sin, cos, pi, degrees
import pyray
from ui.window import *
from util.vector2 import IntVec2
from geometry.loop import Loop, test_intersections
from geometry.loop_system import Cell, LoopSystem

class CellView:
	def __init__(self, loop):
		self.loop_system = LoopSystem(Cell(loop))
		self.message = None

	def update(self):
		mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())
		points = [mouse_pos + IntVec2(100, 0)]

		for i in range(1, 4):
			angle = i * pi / 2
			next_point = mouse_pos + IntVec2(100 * cos(angle), 100 * sin(angle))
			points.append((points[-1] + next_point) // 2)
			points.append(next_point)

		points.append((points[0] + points[-1]) // 2)
		self.new_loop = Loop.from_points(points)

		if pyray.is_mouse_button_pressed(0):
			try:
				self.loop_system.add_loop(self.new_loop)
			except NotImplementedError as e:
				self.message = f"Unimplemented: {e}"
			else:
				self.message = ""

		assert len(self.new_loop.curves) == 4
		assert self.new_loop.calculate_turning_number() == 1

	def draw(self):
		a = ("123434"
			"6789")
		assert(a == "1234346789")
		self.loop_system.draw(main_color)
		self.new_loop.draw(main_color)

		if self.message:
			pyray.draw_text(self.message, 50, 50, 30, pyray.RED)

		# Debug stuff:

		# global test_intersections
		# for i, intersection in enumerate(test_intersections):
		# 	color = [pyray.RED, pyray.BLUE][i & 1]

		# 	pyray.draw_text(str(intersection), 50, 100 + 50*i, 20, color)
		# 	intersection.draw(color)

		# n = 10 * len(self.loop_system.cells[0].main_loop.curves)
		# for i in range(n):
		# 	pos = self.loop_system.cells[0].main_loop.eval(i / 10)

		# 	c = i * 255 // n
		# 	pyray.draw_circle_lines(pos.x, pos.y, 10, pyray.Color(c, c, c, 255))

