from dash import dcc, html
import numpy as np
from util.selectors.selector import Selector

SLIDER_OPT_AMOUNT = 30
SLIDER_MARK_AMOUNT = 5

class LogSlider(Selector):
	def __init__(self, name, min, state, max, custom_constraints=id):
		self.name = name
		self.min = min
		self.state = state
		self.max = max

		self.id = None

		self.log_max = np.log10(self.max)
		self.log_min = np.log10(self.min)
		
		
	def calculate_step(self):
		step = (self.log_max - self.log_min) / SLIDER_OPT_AMOUNT
		return step

	def calculate_marks(self):
		marks = {}
		step = (self.log_max - self.log_min) / SLIDER_MARK_AMOUNT

		for i in range(SLIDER_MARK_AMOUNT + 1):
			position = self.log_min + i * step

			if position % 1 == 0: # it doesnt like float keys for "integer" values
				position = int(position)
			else:
				position = float(position)

			value = int(self.transfrom_up(position)) if float(self.transfrom_up(position)).is_integer() else float(self.transfrom_up(position))
			marks[position] = f"{value:.6g}" # 6 significant digits
		return marks

	@staticmethod
	def round_nice_number(x):
		# rounds to "nice" number with less than ~5% error
		if x == 0:
			return 0
		sign = np.sign(x)
		x = abs(x)

		# step ~10% of x => ~5% rounding error
		step = (10 ** np.floor(np.log10(x))) / 10
		nice = sign * round(x / step) * step

		return int(nice) if float(nice).is_integer() else nice
	
	# same as transform_pow_10 in tooltip.js
	def transfrom_up(self, value):
		return LogSlider.round_nice_number(10 ** value)
	
	# not quite the inverse of transfrom_up due to rounding
	def transfrom_down(self, value):
		if value <= 0:
			return 0
		return np.log10(value)

	def to_dash_component(self, _type, id):
		self.id = id
		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id={"type": _type, "index": id},
				min=self.log_min,
				max=self.log_max,
				value=self.transfrom_down(self.state),
				tooltip={"placement": "bottom", "always_visible": True, "transform": "transform_log_nice"},
				step=self.calculate_step(),
				marks=self.calculate_marks(),
				updatemode="drag",
			)
		])
	
	def update_state(self, new_state):
		self.state = self.transfrom_up(new_state)