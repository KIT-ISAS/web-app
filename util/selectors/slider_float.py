from dash import dcc, html
from util.selectors.selector import Selector

SLIDER_OPT_AMOUNT = 100
SLIDER_MARK_AMOUNT = 5

class FloatSlider(Selector):
	def __init__(self, name, min, state, max, transform_tooltip=None):
		self.name = name
		self.min = min
		self.state = state
		self.max = max

		self.id = None
		self.transform_tooltip = transform_tooltip


	def to_dash_component(self, _type, id, renderer_id):
		if self.transform_tooltip is None:
			tooltip = {"placement": "bottom", "always_visible": True}
		else:
			tooltip = {"placement": "bottom", "always_visible": True, "transform": self.transform_tooltip}

		self.id = id
		return html.Div([
			html.Label(self.name),

			dcc.Slider(
				id={"type": _type, "index": id, "renderer": renderer_id},
				min=self.min,
				max=self.max,
				value=self.state,
				tooltip=tooltip,
				updatemode="drag",
			)
		])
	
	def update_state(self, new_state):
		self.state = new_state
