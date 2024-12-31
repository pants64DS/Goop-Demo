import pyray
import ui

if __name__ == "__main__":
	pyray.init_window(ui.screen_width, ui.screen_height, "Goop Demo")
	pyray.enable_event_waiting()

	float_curve_view = ui.FloatCurveView()
	float_loop_view = ui.FloatLoopView()
	pixel_view = ui.PixelView()
	curve_view = ui.CurveView()

	curr_view = curve_view
	while not pyray.window_should_close():
		if pyray.is_key_pressed(pyray.KEY_ONE):
			curr_view = float_curve_view

		if pyray.is_key_pressed(pyray.KEY_TWO):
			curr_view = float_loop_view

		if pyray.is_key_pressed(pyray.KEY_THREE) and curr_view is float_loop_view:
			curr_view = ui.FloatCellView(float_loop_view.loop)

		if pyray.is_key_pressed(pyray.KEY_FOUR):
			curr_view = pixel_view

		if pyray.is_key_pressed(pyray.KEY_FIVE):
			curr_view = curve_view

		curr_view.update()
		pyray.begin_drawing()
		pyray.clear_background(ui.bg_color)
		curr_view.draw()
		pyray.end_drawing()

	pyray.close_window()
