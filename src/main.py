import pyray
import ui

if __name__ == "__main__":
	pyray.init_window(ui.screen_width, ui.screen_height, "Goop Demo")
	pyray.enable_event_waiting()

	curve_view = ui.CurveView()
	loop_view = ui.LoopView()

	curr_view = loop_view
	while not pyray.window_should_close():
		if pyray.is_key_pressed(pyray.KEY_ONE):
			curr_view = curve_view

		if pyray.is_key_pressed(pyray.KEY_TWO):
			curr_view = loop_view

		if pyray.is_key_pressed(pyray.KEY_THREE) and curr_view is loop_view:
			curr_view = ui.CellView(loop_view.loop)

		curr_view.update()
		pyray.begin_drawing()
		pyray.clear_background(ui.bg_color)
		curr_view.draw()
		pyray.end_drawing()

	pyray.close_window()
