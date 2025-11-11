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
