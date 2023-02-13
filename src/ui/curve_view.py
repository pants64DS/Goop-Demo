import pyray
from ui.window import *
from geometry.curve import Curve
from ui.button import Button, ButtonSystem
from util.vector2 import IntVec2

class CurveView:
	def __init__(self):
		self.buttons = ButtonSystem(
			Button(256, 56),
			Button(508, 290),
			Button(142, 634),
			Button(950, 60),
			Button(620, 508),
			Button(1010, 546)
		)

	def update(self):
		self.buttons.update()
		self.curve1 = Curve(*[self.buttons[i].pos for i in range(0, 3)])
		self.curve2 = Curve(*[self.buttons[i].pos for i in range(3, 6)])
		self.intersections = self.curve1.find_intersections(self.curve2)

		self.mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())

		y_coords1 = self.curve1.find_vertical_line_intersections(self.mouse_pos.x)
		y_coords2 = self.curve2.find_vertical_line_intersections(self.mouse_pos.x)

		self.intersections += [IntVec2(self.mouse_pos.x, y) for y in y_coords1]
		self.intersections += [IntVec2(self.mouse_pos.x, y) for y in y_coords2]

	def draw(self):
		self.curve1.draw(main_color)
		self.curve2.draw(main_color)

		self.curve1.draw_lines(pyray.RED)
		self.curve2.draw_lines(pyray.RED)

		pyray.draw_line(self.mouse_pos.x, 0, self.mouse_pos.x, screen_height, main_color)

		self.buttons.draw()

		for intersection in self.intersections:
			pyray.draw_circle_lines(int(intersection.x), int(intersection.y), 10, pyray.RED)
