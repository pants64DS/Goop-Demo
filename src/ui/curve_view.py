import pyray
import ui
from geometry import make_curve
from util import IntVec2

class CurveView:
	def __init__(self):
		self.buttons = ui.ButtonSystem(
			ui.Button(256, 56),
			ui.Button(508, 290),
			ui.Button(142, 634),
			ui.Button(950, 60),
			ui.Button(620, 508),
			ui.Button(1010, 546)
		)

	def update(self):
		self.buttons.update()
		self.curve1 = make_curve(*[self.buttons[i].pos for i in range(0, 3)])
		self.curve2 = make_curve(*[self.buttons[i].pos for i in range(3, 6)])
		self.intersections = self.curve1.find_intersections(self.curve2)

		self.mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())

		# y_coords1 = self.curve1.find_vertical_line_intersections(self.mouse_pos.x)
		# y_coords2 = self.curve2.find_vertical_line_intersections(self.mouse_pos.x)

		# self.intersections += [IntVec2(self.mouse_pos.x, y) for y in y_coords1]
		# self.intersections += [IntVec2(self.mouse_pos.x, y) for y in y_coords2]

	def draw(self):
		self.curve1.draw(ui.main_color)
		self.curve2.draw(ui.main_color)

		self.curve1.draw_lines(pyray.RED)
		self.curve2.draw_lines(pyray.RED)

		# pyray.draw_line(self.mouse_pos.x, 0, self.mouse_pos.x, ui.screen_height, ui.main_color)

		self.buttons.draw()

		for intersection in self.intersections:
			x, y = intersection.get_pos()
			pyray.draw_circle_lines(x, y, 10, pyray.RED)
