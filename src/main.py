import pyray
from ui.window import *
from ui.curve_view import CurveView
from ui.loop_view import LoopView

if __name__ == "__main__":
	pyray.init_window(screen_width, screen_height, "Goop Demo")
	pyray.enable_event_waiting()

	views = CurveView(), LoopView()
	curr_view_id = 0
	while not pyray.window_should_close():
		if pyray.is_key_pressed(pyray.KEY_ONE):
			curr_view_id = 0

		if pyray.is_key_pressed(pyray.KEY_TWO):
			curr_view_id = 1

		views[curr_view_id].update()
		pyray.begin_drawing()
		pyray.clear_background(bg_color)
		views[curr_view_id].draw()
		pyray.end_drawing()

	pyray.close_window()
