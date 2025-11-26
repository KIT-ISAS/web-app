from dash import dcc, html
import numpy as np
from util.selectors.selector import Selector
import sympy as sp


SLIDER_MARK_AMOUNT = 5
"""
Silder that only selects Fibonacci numbers within a given range.
min and max are the indices in the Fibonacci sequence.
state is not an index, but the actual Fibonacci number at a valid index.
"""
class SliderFib(Selector):
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
				tooltip={"placement": "bottom", "always_visible": True, "transform": "transform_fib"},
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
			marks[value] = str(sp.fibonacci(value))
		return marks

	
	def update_state(self, new_state):
		self.state = int(sp.fibonacci(new_state))
		self.idx = int(new_state)

	def transfrom_up(self, x):
		return int(sp.fibonacci(x))
	
	def transfrom_down(self, x):
		for i in range(0, x + 1):
			if sp.fibonacci(i) == x:
				return i
		raise ValueError(f"{x} is not a Fibonacci number")
	
	@staticmethod
	def is_valid(n):
		if n < 0:
			return False
		# A number is a Fibonacci number if and only if one or both of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square 
		# https://en.wikipedia.org/wiki/Fibonacci_sequence
		test1 = 5 * n * n + 4
		test2 = 5 * n * n - 4

		def is_perfect_square(x):
			s = int(np.sqrt(x))
			return s * s == x

		return is_perfect_square(test1) or is_perfect_square(test2)

	
