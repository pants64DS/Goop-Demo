from geometry import Loop
from ui import draw_area

class LoopSystem:
	def __init__(self, *cells):
		self.cells = cells

	def draw(self, color, thickness=2):
		for cell in self.cells:
			cell.draw(color, thickness)

	def get_curves(self):
		curves = []
		for cell in self.cells:
			curves += cell.main_loop.curves
			curves += cell.inner_loop_system.get_curves()

		return curves

	def draw_inside(self):
		return draw_area(self.get_curves())

	def cut_loop(self, loop):
		for cell in self.cells:
			if loop.intersects_with(cell.main_loop):
				raise NotImplementedError("Cutting cells with an intersecting loop")

			elif loop.is_inside_nonintersecting(cell.main_loop):
				cell.inner_loop_system.add_loop(loop)
				return

	def add_loop(self, loop):
		outer_cells = [] # Cells that are outside of loop
		edge_cells = []  # Cells that intersect with loop

		for cell in self.cells:
			if loop.intersects_with(cell.main_loop):
				edge_cells.append(cell)
			elif loop.is_inside_nonintersecting(cell.main_loop):
				cell.inner_loop_system.cut_loop(loop)
				return
			elif cell.main_loop.is_outside_nonintersecting(loop):
				outer_cells.append(cell)

		print(f"edge cells: {len(edge_cells)}")
		bounding_loop, new_holes = loop.merge_to([cell.main_loop for cell in edge_cells])
		print(f"bounding loop curves: {len(bounding_loop.curves)}")

		bounding_loop_insides = LoopSystem()
		for cell in edge_cells:
			bounding_loop_insides.cells += cell.inner_loop_system.cells

		bounding_loop_insides.cut_loop(loop)

		for new_hole in new_holes:
			cells_in_new_hole = []

			for i, outer_cell in enumerate(outer_cells):
				if outer_cell.is_inside_nonintersecting(new_hole):
					cells_in_new_hole.append(outer_cell)
					outer_cells[i] = None

			bounding_loop_insides.cells.append(Cell(new_hole, LoopSystem(*cells_in_new_hole)))

		self.cells = [Cell(bounding_loop, bounding_loop_insides)]

		for outer_cell in outer_cells:
			if outer_cell is not None:
				self.cells.append(outer_cell)

	# def cut_loop(self, cutter: Loop):

class Cell:
	def __init__(self, main_loop, inner_loop_system=LoopSystem()):
		self.main_loop = main_loop
		self.inner_loop_system = inner_loop_system

	def draw(self, color, thickness=2):
		self.inner_loop_system.draw(color, thickness)
		self.main_loop.draw(color, thickness)
