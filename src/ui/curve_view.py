import pyray
import ui
from util import IntVec
from exact_geometry import curve_intersection

res_strings = {
	True:  "the curves intersect",
	False: "no intersection",
	None:  "unimplemented"
}

class CurveView:
	def __init__(self):
		self.buttons = ui.ButtonSystem(
			ui.Button(ui.center_x -  60, ui.center_y + 180, pyray.RED),
			ui.Button(ui.center_x - 350, ui.center_y - 200, pyray.GREEN),
			ui.Button(ui.center_x + 350, ui.center_y + 100, pyray.YELLOW),
			ui.Button(ui.center_x +  60, ui.center_y - 180, pyray.BLUE),
			ui.Button(ui.center_x + 350, ui.center_y + 200, pyray.BLUE),
			ui.Button(ui.center_x - 350, ui.center_y - 100, pyray.BLUE)
		)
		self.case_id = None
		self.result = None

	def draw_curves(self):
		positions = [button.pos.to_pyray_vector2() for button in self.buttons]
		pyray.draw_line_bezier_quad(positions[0], positions[2], positions[1], 2, pyray.RED)
		pyray.draw_line_bezier_quad(positions[3], positions[5], positions[4], 2, pyray.BLUE)

	def draw_line(self, p0, p1):
		a = p1 - p0
		w = ui.screen_width
		h = ui.screen_height

		if p0[0] == p1[0]:
			y_left = y_right = -1
		else:
			y_left   = p0[1] -  p0[0]      * a[1] / a[0]
			y_right  = p0[1] - (p0[0] - w) * a[1] / a[0]

		if p0[1] == p1[1]:
			x_top = x_bottom = -1
		else:
			x_top    = p0[0] -  p0[1]      * a[0] / a[1]
			x_bottom = p0[0] - (p0[1] - h) * a[0] / a[1]

		endpoints = []

		if 0 <= x_top    <= w: endpoints.append((x_top, 0))
		if 0 <= x_bottom <= w: endpoints.append((x_bottom, h))

		if len(endpoints) == 0:
			endpoints.append((0, y_left))
			endpoints.append((w, y_right))
		elif len(endpoints) == 1:
			if 0 <= y_left  <= h:
				endpoints.append((0, y_left))
			else:
				endpoints.append((w, y_right))

		pyray.draw_line_ex(*endpoints, 2, pyray.RED)

	def update(self):
		self.buttons.update()
		positions = [button.pos for button in self.buttons]
		self.case_id, self.result = curve_intersection(*positions)

	def draw(self):
		self.draw_curves()
		self.draw_line(self.buttons[0].pos, self.buttons[2].pos)
		msg = f"case {self.case_id}, {res_strings[self.result]}"
		pyray.draw_text(msg, 30, 30, 20, pyray.RED)

		for button in self.buttons:
			button.draw()
