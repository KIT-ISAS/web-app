from dataclasses import dataclass

@dataclass
class PlotSettings2D:
	axes_2d_x: tuple
	axes_2d_y: tuple
	lock_aspect_ratio: bool

	periodic_x: bool = False
	periodic_y: bool = False
	periodic_x_amount: float = 0.0 # amount to shift for periodicity
	periodic_y_amount: float = 0.0

	x_title: str = "" # title for axis
	y_title: str = ""

	reverse_x_y_axis: bool = False # if set to True in the (n,2) shaped data, first column is y and second is x
