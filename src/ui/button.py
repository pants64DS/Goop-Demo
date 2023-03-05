import pyray
from util import IntVec
import ui

class Button:
	def __init__(self, x, y, color = ui.main_color, radius = 10):
		self.pos = IntVec(x, y)
		self.color = color
		self.radius = radius
		self.click_offset = IntVec(0, 0)
		self.clicked = False

	def click(self, clicked_pos):
		offset = self.pos - IntVec(clicked_pos.x, clicked_pos.y)

		if offset.length() <= self.radius:
			self.click_offset = offset
			self.clicked = True
			return True
		return False

	def update_pos(self, mouse_pos):
		if not self.clicked:
			return

		self.pos = IntVec(mouse_pos.x, mouse_pos.y) + self.click_offset

		if self.pos.x < self.radius: self.pos.x = self.radius
		if self.pos.y < self.radius: self.pos.y = self.radius

		max_x = ui.screen_width - self.radius
		max_y = ui.screen_height - self.radius

		if self.pos.x > max_x: self.pos.x = max_x
		if self.pos.y > max_y: self.pos.y = max_y

	def unclick(self):
		self.clicked = False

	def draw(self):
		if self.clicked:
			pyray.draw_circle(*self.pos, self.radius, self.color)
		else:
			pyray.draw_circle_lines(*self.pos, self.radius, self.color)

class ButtonSystem:
	def __init__(self, *buttons):
		self.buttons = buttons

	def update(self):
		if pyray.is_mouse_button_pressed(0):
			mouse_pos = pyray.get_mouse_position()
			for button in self.buttons:
				if button.click(mouse_pos):
					break

		if pyray.is_mouse_button_released(0):
			for button in self.buttons:
				button.unclick()

		if pyray.is_mouse_button_down(0):
			mouse_pos = pyray.get_mouse_position()
			for button in self.buttons:
				button.update_pos(mouse_pos)

	def draw(self):
		for button in self.buttons:
			button.draw()

	def __getitem__(self, key):
		return self.buttons.__getitem__(key)
