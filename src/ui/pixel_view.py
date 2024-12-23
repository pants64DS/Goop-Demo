import pyray
from digital_geometry import Curve
import ui
from util import IntVec, sort

class PixelView:
	def __init__(self):
		self.half_grid_size = 8

		self.buttons = ui.ButtonSystem(
			ui.Button(*self.to_screen_coords(( -6,  18)), pyray.Color(255, 255, 0, 255)),
			ui.Button(*self.to_screen_coords((-35, -20)), pyray.Color(255, 255, 0, 255)),
			ui.Button(*self.to_screen_coords(( 35,  10)), pyray.Color(255, 255, 0, 255))
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

		try:
			pixels = [point for point in self.curve]
		except Exception as e:
			print(f"ERROR!!!!!!: {e}")
			pixels = []

		yellow = pyray.Color(255, 255, 0, 255)
		red    = pyray.Color(255, 0, 0, 255)

		for i, pixel in enumerate(pixels):
			self.draw_pixel(pixel, red)

		self.draw_continous_curve(self.curve, yellow)

		p0 = self.curve.p0 - self.curve.p1
		p2 = self.curve.p2 - self.curve.p1

		if p0.x * p2.y == p0.y * p2.x:
			pyray.draw_text("The control points are collinear", 30, 30, 20, yellow)

		if p0.x + p2.x == 0:
			pyray.draw_text("The x-function is affine", 30, 50, 20, red)

		if p0.y + p2.y == 0:
			pyray.draw_text("The y-function is affine", 30, 70, 20, red)

		for button in self.buttons:
			button.draw()
