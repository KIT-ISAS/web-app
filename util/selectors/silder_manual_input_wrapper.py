from util.selectors.selector import Selector
from dash import dcc, html, callback, Input, Output, ALL


class SliderManualInputWrapper():
	def __init__(self, slider, check_input):
		self.id = None # unique id for dash callback
		self.slider = slider
		self.check_input = check_input

	def to_dash_component(self, _type, id, renderer_id):
		slider_component = self.slider.to_dash_component(_type, id, renderer_id)
		self.id = id
		self.renderer_id = renderer_id
		
		component = html.Div([
			html.Div(
				children=[slider_component],
				#style={"flex": "1"}
				style={"display": "inline-block", "width": r"calc(100% - 5rem)", "verticalAlign": "bottom"}
			),
			html.Div(
				children=[dcc.Input(
					id={"type": f"manual_input-{_type}", "index": id, "renderer": renderer_id},
					type="number",
					value=self.slider.state,
					#style={"width": "5rem"},
					style={"width": "100%"},
				)],
				style={"display": "inline-block", "width": "5rem", "verticalAlign": "bottom", "margin-bottom": "1rem"}
			),
			
		])
		return component
	
	def update_state(self, new_state): # only called by slider callback, gauranteed valid
		self.slider.update_state(new_state)

	def update_state_manual(self, manual_value):
		#Update from a manual text/number input; converts to slider domain if needed."""
		if hasattr(self.slider, "transfrom_down"):
			slider_value = self.slider.transfrom_down(manual_value)
		else:
			slider_value = manual_value

		self.slider.update_state(slider_value)
		return slider_value

	@property
	def state(self):
		return self.slider.state
