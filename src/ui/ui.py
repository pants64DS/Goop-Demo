from math import floor
import pyray

bg_color = pyray.Color(30, 32, 44, 255)
main_color = pyray.Color(156, 158, 232, 255)
fill_color = pyray.Color(110, 110, 180, 255)
screen_width = 1280
screen_height = 720

def draw_area(curves):
	line_gap = 14
	total_width = screen_width + screen_height
	num_lines = total_width // line_gap

	intersections = [[] for i in range(num_lines)]

	for og_curve in curves:
		sheared_curve = og_curve.transformed(lambda p: (p.x + p.y, p.y))

		bbox = sheared_curve.get_bounding_box()
		left_x = max(bbox.left_x // line_gap * line_gap, line_gap)
		right_x = min(bbox.right_x // -line_gap * -line_gap, total_width)

		for x in range(left_x, right_x + 1, line_gap):
			i = x // line_gap - 1

			if x == sheared_curve.p0.x and sheared_curve.starts_going_left():
				intersections[i].append(sheared_curve.p0.y)

			if x == sheared_curve.p2.x and sheared_curve.ends_going_left():
				intersections[i].append(sheared_curve.p2.y)

			for t in sheared_curve.find_vertical_line_intersections(x):
				intersections[i].append(floor(sheared_curve.eval_y(t)))

	for i, l in enumerate(intersections):
		l.sort()
		x = (i + 1) * line_gap
		for j in range(0, len(l) - 1, 2):
			start_y = l[j]
			end_y = l[j + 1]

			if start_y != end_y:
				pyray.draw_line(x - start_y, start_y, x - end_y, end_y, fill_color)

