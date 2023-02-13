from math import sin, cos, pi
import pyray
from ui.window import *
from util.vector2 import IntVec2
from geometry.curve import Curve
from geometry.loop import Loop
from ui.button import Button, ButtonSystem
from ui.window import *

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

		self.loop = Loop([button.pos for button in self.buttons])
		mouse_pos = IntVec2.from_pyray_vector2(pyray.get_mouse_position())

		try:
			if self.loop.is_point_inside(mouse_pos):
				self.message = "Inside"
			else:
				self.message = "Outside"
		except NotImplementedError:
			self.message = "Scenario unimplemented"

	def draw(self):
		self.loop.draw(main_color)
		self.buttons.draw()

		pyray.draw_text(self.message, 20, 20, 30, pyray.RED)
