from dataclasses import dataclass

@dataclass
class PlotSettings2D:
	axes_2d_x: tuple
	axes_2d_y: tuple
	lock_aspect_ratio: bool
