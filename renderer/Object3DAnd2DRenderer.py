from dash import html, dcc, callback, Input, Output, ALL, State, Patch, no_update
import plotly.graph_objects as go

from renderer.Object3DRenderer import Object3DRenderer

class Object3DAnd2DRenderer(Object3DRenderer):
	def __init__(self, object, id):
		# the renderer starts out in 3d mode
		super().__init__(object, id, register_3d_callbacks=False)
		self.register_plot_callbacks()
		self.register_mode_callbacks()

		self.fig_2d = go.Figure()

	def register_plot_callbacks(self):
		# updates the plot based on selected sampling options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			State(f"mode-selector-{self.id}", "value"),
			Input(f"mode-done-{self.id}", "data"),
			Input({"type": "dist", "index": ALL}, "value"),
			State({"type": "dist", "index": ALL}, "id"),
			Input({"type": "sampling", "index": ALL}, "value"),
			State({"type": "sampling", "index": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_sample_callback(mode, _mode_counter, values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _):
			if mode == "3D View":
				return self.update_plot_sample(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _)
			else:
				return self.update_plot_sample_2d(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _)
		
		# updates the plot based on selected distribution options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			State(f"mode-selector-{self.id}", "value"),
			Input(f"mode-done-{self.id}", "data"),
			Input({"type": "dist", "index": ALL}, "value"),
			State({"type": "dist", "index": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_dist_callback(mode, _mode_counter, values_dist, ids_dist, selected_distribution, selected_sampling, _):
			if mode == "3D View":
				return self.update_plot_dist(values_dist, ids_dist, selected_distribution, selected_sampling, _)
			else:
				return self.update_plot_dist_2d(values_dist, ids_dist, selected_distribution, selected_sampling, _)
	

	def register_mode_callbacks(self):
		@callback(
			Output(f"graph-{self.id}", "figure"),
			Output(f"mode-done-{self.id}", "data"),
			Input(f"mode-selector-{self.id}", "value"),
			State(f"mode-done-{self.id}", "data"),
		)
		def switch_mode(mode, data):
			new_data = (data + 1 if data is not None else 1)
			if mode == "3D View":
				return self.fig, new_data
			else:
				return self.fig_2d, new_data

	def update_plot_sample_2d(self, values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _):
		return no_update

	def update_plot_dist_2d(self, values_dist, ids_dist, selected_distribution, selected_sampling, _):
		return no_update

	def get_layout_components(self):
		initial_distribution = self.object.distributions[list(self.object.distributions.keys())[0]]
		initial_sampling_method = initial_distribution.sampling_methods[0].get_name() if initial_distribution.sampling_methods else "no sampling methods found"
		initial_sampling_options = [x.get_name() for x in initial_distribution.sampling_methods]
		
		options = [
			html.P("Select Visualization Mode:"),

			# needed to create dependecy between mode selector and plot update callbacks
			# to insure they are fired after the plot mode finished changing
			# data is just a counter that is incremented each time the mode is changed,
			# so dash detects a change and fires callbacks depending on it (update samp and dist)
			dcc.Store(id=f"mode-done-{self.id}", data=0), 
			
			dcc.RadioItems(
				id=f"mode-selector-{self.id}",
				options=["3D View", "2D View"],
				value="3D View",
				inline=True,
				labelStyle={"marginRight": "15px"}
			),
			html.Hr(),
			html.Br(),
			html.P("Select Distribution and Sampling Method:"),
			dcc.RadioItems(
				id="distribution-selector",
				options=(list(self.object.distributions.keys())),
				value=initial_distribution.get_name() if self.object.distributions else "no distributions found",
			),
			html.Br(),
			dcc.RadioItems(
				id=f"sampling-selector-{self.id}",
				options=(list(initial_sampling_options)),
				value=initial_sampling_method,
			),
			html.Br(),
			html.Hr(),
			html.Br(),

			html.Div(id=f"distribution-options-{self.id}"),
			html.Div(id=f"sampling-options-{self.id}"),
		]

		graph = [dcc.Graph(id=f"graph-{self.id}", figure=self.fig, config=self.config, style={'height': '100%'})]

		return options, graph