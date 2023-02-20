from math import sin, cos, pi, degrees
import pyray
from ui.window import *
from util.vector2 import IntVec2
from geometry.curve import Curve
from geometry.loop import Loop
from ui.button import Button, ButtonSystem

class LoopView:
	def __init__(self):
		mid = IntVec2(screen_width, screen_height) // 2
		points = [mid + IntVec2(300, 0)]

		for i in range(1, 6):
			angle = i * pi / 3
			next_point = mid + IntVec2(300 * cos(angle), 300 * sin(angle))
			points.append((points[-1] + next_point) // 2)
			points.append(next_point)

		points.append((points[0] + points[-1]) // 2)

		self.buttons = ButtonSystem(*[Button(*point) for point in points])

	def update(self):
		self.buttons.update()

		self.loop = Loop.from_points([button.pos for button in self.buttons])
		self.mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())

		try:
			if self.loop.is_point_inside(self.mouse_pos):
				self.message = "Inside"
				self.message_color = pyray.YELLOW
			else:
				self.message = "Outside"
				self.message_color = pyray.RED

		except NotImplementedError as e:
			self.message = f"Unimplemented: {e}"
			self.message_color = pyray.RED

		self.turning_angle = f"Sum of turning angles: {int(degrees(self.loop.calculate_turning_angle()))}°"

	def draw(self):
		self.loop.draw(main_color)
		self.loop.draw_lines()
		self.buttons.draw()

		text_x = self.mouse_pos.x + 10
		text_y = self.mouse_pos.y - 30
		pyray.draw_text(self.message, text_x, text_y, 20, self.message_color)
		pyray.draw_text(self.turning_angle, 50, 50, 30, pyray.RED)
