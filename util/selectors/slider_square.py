from dash import dcc, html
import numpy as np
from util.selectors.selector import Selector
import sympy as sp


SLIDER_MARK_AMOUNT = 5
"""
Silder that only selects perfect squares within a given range.
min and max are the indices of the square (eg. i^2).
state is not an index, but the actual Square number at a valid index.
"""
class SliderSquare(Selector):
	def __init__(self, name, min, state, max, idx):
		self.name = name
		self.min = min
		self.state = state
		self.idx = idx
		self.max = max

		self.id = None

	def to_dash_component(self, _type, id, renderer_id):
		self.id = id
		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id={"type": _type, "index": id, "renderer": renderer_id},
				min=self.min,
				max=self.max,
				value=self.idx,
				tooltip={"placement": "bottom", "always_visible": True, "transform": "transform_square"},
				step=1,
				marks=self.calculate_marks(),
				updatemode="drag",
			)
		])
	
	def calculate_marks(self):

		marks = {}
		step = (self.max - self.min) / SLIDER_MARK_AMOUNT
		for i in range(SLIDER_MARK_AMOUNT + 1):
			value = int(self.min + i * step)
			marks[value] = str((value**2))
		return marks

	
	def update_state(self, new_state):
		self.state = int((new_state**2))
		self.idx = int(new_state)

	def transfrom_up(self, x):
		return int((x**2))
	
	def transfrom_down(self, x):
		for i in range(0, int(np.sqrt(x)) + 1):
			if (i**2) == x:
				return i
		raise ValueError(f"{x} is not a perfect square number")

	@staticmethod
	def is_valid(x):
		s = int(np.sqrt(x))
		return s * s == x
