from dash import dcc, html
from util.selectors.selector import Selector

SLIDER_OPT_AMOUNT = 100
SLIDER_MARK_AMOUNT = 5

class Slider(Selector):
	def __init__(self, name, min, state, max):
		self.name = name
		self.min = min
		self.state = state
		self.max = max
		
		
	def calculate_step(self):
		# rounds down to the neares human readable step
		# eg. 1,5,25,50,100,250,500,1000, ...

		step_unrounded = (self.max - self.min) // SLIDER_OPT_AMOUNT
		sequence = [1, 5, 25, 50]

		prev = 1

		while True:
			for s in sequence:
				if step_unrounded < s:
					return prev
				prev = s
			sequence = [s * 10 for s in sequence]

	def calculate_marks(self):
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
			marks[value] = str(value)
		return marks


	def to_dash_component(self, id):
		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id={"type": "dynamic-option", "index": id},
				min=self.min,
				max=self.max,
				value=self.state,
				tooltip={"placement": "bottom", "always_visible": True},
				step=self.calculate_step(),
				marks=self.calculate_marks(),
			)
		])
	
	def update_state(self, new_state):
		self.state = int(new_state)