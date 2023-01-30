import pyray
from ui.button import Button
from ui.window import *
from geometry.curve import Curve

pyray.init_window(screen_width, screen_height, "Goop Demo")
pyray.enable_event_waiting()

buttons = [Button(256, 56), Button(508, 290), Button(142, 634), Button(950, 60), Button(620, 508), Button(1010, 546)]

while not pyray.window_should_close():
	if pyray.is_mouse_button_pressed(0):
		mouse_pos = pyray.get_mouse_position()
		for button in buttons:
			if button.click(mouse_pos):
				break

	if pyray.is_mouse_button_released(0):
		for button in buttons:
			button.unclick()

	if pyray.is_mouse_button_down(0):
		mouse_pos = pyray.get_mouse_position()
		for button in buttons:
			button.update_pos(mouse_pos)

	curve1 = Curve(buttons[0].pos, buttons[1].pos, buttons[2].pos)
	curve2 = Curve(buttons[3].pos, buttons[4].pos, buttons[5].pos)

	intersections = curve1.find_intersections(curve2)

	pyray.begin_drawing()
	pyray.clear_background(bg_color)

	curve1.draw(main_color)
	curve2.draw(main_color)

	for intersection in intersections:
		pyray.draw_circle_lines(int(intersection.x), int(intersection.y), 10, pyray.RED)

	for button in buttons:
		button.draw()

	pyray.end_drawing()

pyray.close_window()
