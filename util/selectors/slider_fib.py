from dash import dcc, html
import numpy as np
from util.selectors.selector import Selector
import sympy as sp


SLIDER_MARK_AMOUNT = 5
"""
Silder that only selects Fibonacci numbers within a given range.
min and max are the indices in the Fibonacci sequence.
state is not an index, but the actual Fibonacci number at a valid index.
if minus_1 is set, Fibonacci numbers -1 are used instead. (initial) state is should then also be Fibonacci number -1.
"""
class SliderFib(Selector):
	def __init__(self, name, min, state, max, idx, minus_1=False):
		self.name = name
		self.min = min
		self.state = state
		self.idx = idx
		self.max = max

		self.id = None
		self.minus_1 = minus_1 

	def to_dash_component(self, _type, id, renderer_id, manual=False):
		self.id = id
		slider_id = {"type": _type, "index": id, "renderer": renderer_id, "manual": manual}

		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id=slider_id,
				min=self.min,
				max=self.max,
				value=self.idx,
				tooltip={"placement": "bottom", "always_visible": True, "transform": "transform_fib" if not self.minus_1 else "transform_fib_m1"},
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
			if not self.minus_1:
				marks[value] = str(sp.fibonacci(value))
			else:
				marks[value] = str(sp.fibonacci(value) - 1)
		return marks

	
	def update_state(self, new_state):
		self.state = int(sp.fibonacci(new_state) - (1 if self.minus_1 else 0))
		self.idx = int(new_state)

	def transfrom_up(self, x):
		return int(sp.fibonacci(x) - (1 if self.minus_1 else 0))
	
	def transfrom_down(self, x):
		if self.minus_1:
			x = x + 1

		for i in range(0, x + 3):
			if int(sp.fibonacci(i)) == x:
				return i
		raise ValueError(f"{x} is not a Fibonacci number")
	
	def is_valid(self, n):
		if self.minus_1:
			n = n + 1

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

	
