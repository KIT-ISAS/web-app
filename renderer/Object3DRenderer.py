from dash import html, dcc, callback, Input, Output, ALL, State
import plotly.graph_objects as go
import uuid

class Object3DRenderer:
	def __init__(self, object_3D):
		# dash doesnt like duplicate calback functions
		# so each renderer instance gets a uuid for suffixing
		self.uuid = str(uuid.uuid4()) 

		# objects should have atleast one corresponding distribution
		self.object = object_3D

		self.x, self.y, self.z = self.object.xyz
	


		self.fig = go.Figure(
			data=[
				go.Surface(
					x=self.x, y=self.y, z=self.z,
					colorscale="Viridis",
					showscale=False
				),
				go.Scatter3d(
					x=self.object.samples[:, 0] if self.object.samples.size else [],
					y=self.object.samples[:, 1] if self.object.samples.size else [],
					z=self.object.samples[:, 2] if self.object.samples.size else [],
					mode="markers",
					marker=dict(size=4, color="red")
				)
			]
		)

		self.fig.update_layout(
			scene=dict(
				aspectmode='data',
				xaxis=dict(visible=False),
				yaxis=dict(visible=False),
				zaxis=dict(visible=False),
			),
			margin=dict(l=0, r=0, t=0, b=0)
		)

		self._register_callbacks()

	
	def _register_callbacks(self):


		# updates wich sampling methods are available once distribution is selected
		@callback(
			Output(f"sampling-selector-{self.uuid}", "options"),
			Input("distribution-selector", "value"),
		)
		def update_sampling_methods(selected_distribution):
			options = list(self.object.distributions[selected_distribution].sampling_method_dict.keys())
			return options

		# updates the options (silders, etc) for the selected distribution and sampling method
		@callback(
			Output(f"distribution-options-{self.uuid}", "children"),
			Output(f"sampling-options-{self.uuid}", "children"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.uuid}", "value")
		)
		def update_curr_distribution(selected_distribution, selected_sampling):
			# ids are given in the same order as options_dist and options_sampling
			options_dist = self.object.distributions[selected_distribution].distribution_options
			options_dist_dcc = [opt.to_dash_component(f"dist-{id}") for id, opt in enumerate(options_dist)]

			options_sampling = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling]
			options_sampling_dcc = [opt.to_dash_component(f"sampling-{id}") for id, opt in enumerate(options_sampling.sample_options)]
			return options_dist_dcc, options_sampling_dcc
		
		# updates the plot based on selected options
		@callback(
			Output(f"graph-{self.uuid}", "figure"),
			Input({"type": "dynamic-option", "index": ALL}, "value"),
			State({"type": "dynamic-option", "index": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.uuid}", "value"),
			Input(f"distribution-options-{self.uuid}", "children"),
		)
		def update_plot(values, ids, selected_distribution, selected_sampling, _):
			dist_options =  self.object.distributions[selected_distribution].distribution_options
			sampling_options = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling].sample_options

			# the order of options might not be guaranteed, so we map them by their ids
			id_value = {id_["index"]: v for id_, v in zip(ids, values)}
			options_samp = [(k, v) for k, v in id_value.items() if str(k).startswith("sampling-")]
			options_dist = [(k, v) for k, v in id_value.items() if str(k).startswith("dist-")]

			# and them sort them, so they are in the same order as sampling_options and dist_options
			options_samp = sorted(options_samp, key=lambda x: int(x[0].split("-")[1]))
			options_dist = sorted(options_dist, key=lambda x: int(x[0].split("-")[1]))


			for opt, (id, new_state) in zip(sampling_options, options_samp):
				opt.update_state(new_state)

			for opt, (id, new_state) in zip(dist_options, options_dist):
				opt.update_state(new_state)

			self.object.update_sample(selected_distribution, selected_sampling, sampling_options, dist_options)

			data =  [
				go.Surface(
					x=self.x, y=self.y, z=self.z,
					showscale=False,
					colorscale="Viridis",
				),
				go.Scatter3d(
					x=self.object.samples[:, 0],
					y=self.object.samples[:, 1],
					z=self.object.samples[:, 2],
					mode="markers",
					marker=dict(size=4, color="red")
				)
			]
			return go.Figure(data=data, layout=self.fig.layout)
		
	def get_layout_components(self):
		initial_distribution = self.object.distributions[list(self.object.distributions.keys())[0]]
		initial_sampling_method = initial_distribution.sampling_methods[0].get_name() if initial_distribution.sampling_methods else "no sampling methods found"
		initial_sampling_options = [x.get_name() for x in initial_distribution.sampling_methods]
		
		options = [
			html.Br(),
			html.P("Select Distribution and Sampling Method:"),
			dcc.RadioItems(
				id="distribution-selector",
				options=(list(self.object.distributions.keys())),
				value=initial_distribution.get_name() if self.object.distributions else "no distributions found",
			),
			html.Br(),
			dcc.RadioItems(
				id=f"sampling-selector-{self.uuid}",
				options=(list(initial_sampling_options)),
				value=initial_sampling_method,
			),
			html.Br(),
			html.Hr(),
			html.Br(),

			html.Div(id=f"distribution-options-{self.uuid}"),
			html.Div(id=f"sampling-options-{self.uuid}"),
		]

		graph = [dcc.Graph(id=f"graph-{self.uuid}", figure=self.fig)]

		return options, graph