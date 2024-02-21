import pyray
from digital_geometry import Curve
import ui
from util import IntVec, sort

class PixelView:
	def __init__(self):
		self.half_grid_size = 8

		self.buttons = ui.ButtonSystem(
			ui.Button(*self.to_screen_coords(( -6,  18)), pyray.RED),
			ui.Button(*self.to_screen_coords((-35, -20)), pyray.GREEN),
			ui.Button(*self.to_screen_coords(( 35,  10)), pyray.BLUE)
		)

	def to_screen_coords(self, v):
		screen_x = ui.center_x + 2 * v[0] * self.half_grid_size
		screen_y = ui.center_y - 2 * v[1] * self.half_grid_size

		return IntVec(screen_x, screen_y)

	def to_grid_coords(self, v):
		grid_x = (v[0] - ui.center_x + self.half_grid_size) // (self.half_grid_size << 1)
		grid_y = (ui.center_y - v[1] + self.half_grid_size) // (self.half_grid_size << 1)

		return IntVec(grid_x, grid_y)

	def draw_pixel(self, pos, color):
		screen_coords = self.to_screen_coords(pos) - (self.half_grid_size, self.half_grid_size)

		size = 2 * self.half_grid_size - 1
		pyray.draw_rectangle(*screen_coords, size, size, color)

	def draw_number(self, pos, n, color=pyray.BLACK):
		screen_coords = self.to_screen_coords(pos) + (1 - self.half_grid_size, 3 - self.half_grid_size)

		pyray.draw_text(hex(n)[2:].upper(), *screen_coords, 10, color)

	def draw_continous_curve(self, curve, color):
		p0 = self.to_screen_coords(curve.p0)
		p1 = self.to_screen_coords(curve.p1)
		p2 = self.to_screen_coords(curve.p2)

		pyray.draw_line_bezier_quad(
			p0.to_pyray_vector2(),
			p2.to_pyray_vector2(),
			p1.to_pyray_vector2(),
			2, color
		)

	def update(self):
		self.buttons.update()
		self.curve = Curve(*[self.to_grid_coords(button.pos) for button in self.buttons])

	def draw(self):
		x = ui.center_x - self.half_grid_size
		while x > 0:
			pyray.draw_line(x, 0, x, ui.screen_height, ui.main_color)
			x2 = ui.screen_width - x
			pyray.draw_line(x2, 0, x2, ui.screen_height, ui.main_color)
			x -= 2 * self.half_grid_size

		y = ui.center_y - self.half_grid_size
		while y > 0:
			pyray.draw_line(0, y, ui.screen_width, y, ui.main_color)
			y2 = ui.screen_height - y
			pyray.draw_line(0, y2, ui.screen_width, y2, ui.main_color)
			y -= 2 * self.half_grid_size

		min_x = (ui.screen_width  - 2 * self.half_grid_size) // (-4 * self.half_grid_size)
		min_y = (ui.screen_height - 2 * self.half_grid_size) // (-4 * self.half_grid_size)

		"""
		pixels = []
		for x in range(min_x, 1 - min_x):
			for y in range(min_y, 1 - min_y):
				i = 0

				if (x, y) in self.curve:
					pixels.append(IntVec(x, y))
					i += 1

				if self.curve.inner_curve_contains((x, y)):
					self.draw_pixel((x, y), pyray.BLUE)
					i += 1

				if self.curve.outer_curve_contains((x, y)):
					self.draw_pixel((x, y), pyray.GREEN)
					i += 1

				assert i in (0, 1)

		sort(pixels, self.curve.comes_before)
		"""

		try:
			pixels = [point for point in self.curve]
		except:
			pixels = []

		for i, pixel in enumerate(pixels):
			self.draw_pixel(pixel, pyray.Color(255, (i << 8) // len(pixels), 0, 255))
			self.draw_number(pixel, i)

		p0 = self.curve.p0 - self.curve.p1
		p2 = self.curve.p2 - self.curve.p1

		if p0.x * p2.y == p0.y * p2.x:
			pyray.draw_text("The control points are collinear", 30, 30, 20, pyray.RED)

		for button in self.buttons:
			button.draw()
