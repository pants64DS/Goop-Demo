import pyray
import ui
from geometry import make_curve, LinearCurve
from util import IntVec2

class CurveView:
	def __init__(self):
		self.buttons = ui.ButtonSystem(
			ui.Button(256, 56),
			ui.Button(508, 290),
			ui.Button(142, 634),
			ui.Button(950, 60),
			ui.Button(620, 508),
			ui.Button(1010, 546),
			ui.Button(420, 600),
			ui.Button(730, 650),
			ui.Button(750, 80),
			ui.Button(480, 110)
		)

		self.message = None

	def update(self):
		self.buttons.update()
		# self.buttons[0].pos.y &= ~1
		# self.buttons[2].pos.y &= ~1
		# self.buttons[3].pos.y &= ~1
		# self.buttons[5].pos.y &= ~1

		# self.buttons[1].pos.y = (self.buttons[0].pos.y + self.buttons[2].pos.y) >> 1
		# self.buttons[4].pos.y = (self.buttons[3].pos.y + self.buttons[5].pos.y) >> 1

		self.curves = [
			make_curve(*[self.buttons[i].pos for i in range(0, 3)]),
			make_curve(*[self.buttons[i].pos for i in range(3, 6)]),
			LinearCurve(self.buttons[6].pos, self.buttons[7].pos),
			LinearCurve(self.buttons[8].pos, self.buttons[9].pos)
		]

		self.intersections = []
		self.message = ""

		for i in range(len(self.curves)):
			for j in range(i + 1, len(self.curves)):
				try:
					self.intersections += self.curves[i].find_intersections(self.curves[j])
				except NotImplementedError as e:
					self.message += f"Unimplemented: {e}\n"

		self.mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())

	def draw(self):
		for curve in self.curves:
			curve.draw(ui.main_color)

		for curve in self.curves:
			curve.draw_lines(pyray.RED)

		self.buttons.draw()

		for intersection in self.intersections:
			x, y = intersection.get_pos()
			pyray.draw_circle_lines(x, y, 10, pyray.RED)

		if self.message:
			pyray.draw_text(self.message, 50, 50, 30, pyray.RED)
