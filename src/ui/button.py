import pyray
from util.vector2 import IntVec2
from ui.window import *

class Button:
	def __init__(self, x, y, color = main_color, radius = 10):
		self.pos = IntVec2(x, y)
		self.color = color
		self.radius = radius
		self.clickOffset = IntVec2(0, 0)
		self.clicked = False

	def click(self, clicked_pos):
		offset = self.pos - IntVec2(clicked_pos.x, clicked_pos.y)

		if offset.length() <= self.radius:
			self.clickOffset = offset
			self.clicked = True
			return True
		return False

	def update_pos(self, mouse_pos):
		if not self.clicked:
			return

		self.pos = IntVec2(mouse_pos.x, mouse_pos.y) + self.clickOffset

		if self.pos.x < self.radius: self.pos.x = self.radius
		if self.pos.y < self.radius: self.pos.y = self.radius

		max_x = screen_width - self.radius
		max_y = screen_height - self.radius

		if self.pos.x > max_x: self.pos.x = max_x
		if self.pos.y > max_y: self.pos.y = max_y

	def unclick(self):
		self.clicked = False

	def draw(self):
		if self.clicked:
			pyray.draw_circle(int(self.pos.x), int(self.pos.y), self.radius, self.color)
		else:
			pyray.draw_circle_lines(int(self.pos.x), int(self.pos.y), self.radius, self.color)
