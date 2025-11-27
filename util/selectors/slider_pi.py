from dash import dcc, html
from util.selectors.selector import Selector
import numpy as np

SLIDER_OPT_AMOUNT = 100
SLIDER_MARK_AMOUNT = 5

class PiSlider(Selector):
	"""
	Slider for values between 0 and 2pi or pi., like FloatSlider but with pi notation on marks.
	min, state, max shall be given relative to pi, eg. min=0, max=2 for 0 to 2pi
	"""
	
	def __init__(self, name, min, state, max, transform_tooltip=None):
		self.name = name
		self.min = min
		self.state = state * np.pi
		self.max = max

		self.id = None
		self.transform_tooltip = transform_tooltip

	def calculate_marks(self):
		# for small marks
		if self.max == 2 and self.min == 0:
			return {
				0: "0",
				0.5: "½π",
				1: "π",
				1.5: "3⁄2π",
				2: "2π"
			}
		if self.max == 1 and self.min == 0:
			return {
				0: "0",
				0.25: "¼π",
				0.5: "½π",
				0.75: "¾π",
				1: "π"
			}


		# for bigger values of pi use clean integer values
		def round_nice_number(x):
			if x >= 1000:
				return round(x, -3)
			elif x >= 100:
				return round(x, -2)
			else:
				return x

		marks = {}
		step = (self.max - self.min) / SLIDER_MARK_AMOUNT
		for i in range(SLIDER_MARK_AMOUNT + 1):
			value = int(self.min + i * step)
			value = round_nice_number(value)
			marks[value] = str(value) + "π"
		return marks


	def to_dash_component(self, _type, id, renderer_id, manual=False):
		if self.transform_tooltip is None:
			tooltip = {
				"placement": "bottom",
				"always_visible": True,
				"template": "{value}π"
			}
		else:
			tooltip = {
				"placement": "bottom",
				"always_visible": True,
				"transform": self.transform_tooltip,
				"template": "{value}π"
			}

		self.id = id
		slider_id = {"type": _type, "index": id, "renderer": renderer_id, "manual": manual}

		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id=slider_id,
				min=self.min,
				max=self.max,
				value=self.transfrom_down(self.state),
				tooltip=tooltip,
				updatemode="drag",
				marks=self.calculate_marks(),
			)
		])
	
	def update_state(self, new_state):
		self.state = self.transfrom_up(new_state)


	def transfrom_up(self, x):
		return x * np.pi
	
	def transfrom_down(self, x):
		return x / np.pi
