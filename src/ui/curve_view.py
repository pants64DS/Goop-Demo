import pyray
import ui
from util import IntVec
from exact_geometry import curve_intersection

res_strings = {
	True:  "the curves intersect",
	False: "no intersection",
	None:  "unimplemented"
}

def get_case_messages(case_id, result):
	messages = []

	if case_id in (1, 2):
		messages.append("The blue curve doesn't intersect the line")

		if case_id == 1:
			messages.append("It's on a different of the line than the red curve")
		else:
			messages.append("It's on the same side of the line as the red curve")

			if result:
				messages.append("It intersects the extended red curve")
			else:
				messages.append("It doesn't intersect the extended red curve")

		return messages

	messages.append("The blue curve intersects the line")

	if case_id == 3:
		messages.append("Its endpoints are on the opposite side of the line as the red curve")

		if result:
			messages.append("The red curve intersects the extended blue curve")
		else:
			messages.append("The red curve doesn't intersect the extended blue curve")

		return messages

	if case_id in (4, 5, 6):
		messages.append("Its endpoints are on the same side of the line as the red curve")

		if case_id == 4:
			messages.append("Its endpoints are between the line and red curve")

			if result:
				messages.append("The red curve intersects the extended blue curve more than twice")
			else:
				messages.append("The red curve intersects the extended blue curve twice or less")

		if case_id == 5:
			messages.append("Its endpoints are on the outer side of the red curve")

	return messages

class CurveView:
	def __init__(self):
		self.buttons = ui.ButtonSystem(
			ui.Button(ui.center_x -  60, ui.center_y + 180, pyray.RED),
			ui.Button(ui.center_x - 350, ui.center_y - 200, pyray.RED),
			ui.Button(ui.center_x + 350, ui.center_y + 100, pyray.RED),
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
		msg = f"Case {self.case_id}, {res_strings[self.result]}:"
		pyray.draw_text(msg, 30, 30, 20, pyray.RED)

		y = 60
		for case_msg in get_case_messages(self.case_id, self.result):
			pyray.draw_text(f"- {case_msg}.", 30, y, 20, pyray.GRAY)
			y += 25

		self.draw_curves()
		self.draw_line(self.buttons[0].pos, self.buttons[2].pos)

		for button in self.buttons:
			button.draw()
