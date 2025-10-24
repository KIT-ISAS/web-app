from functools import lru_cache
from dash import html, dcc, callback, Input, Output, ALL, State, Patch
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
class Object3DRenderer:
	def __init__(self, object_3D, id):
		# dash doesnt like duplicate calback functions
		# so each renderer instance gets a uuid for suffixing
		self.id = id

		# objects should have atleast one corresponding distribution
		self.object = object_3D

		self.x, self.y, self.z = self.object.xyz
	

		# inital figure
		self.fig = go.Figure(
			data=[
				go.Surface(
					name="Surface",
					x=self.x, y=self.y, z=self.z,
					colorscale="Viridis",
					showscale=False,
					showlegend=True,
				),
				go.Scatter3d(
					name="Samples",
					x=self.object.samples[:, 0] if self.object.samples.size else [],
					y=self.object.samples[:, 1] if self.object.samples.size else [],
					z=self.object.samples[:, 2] if self.object.samples.size else [],
					mode="markers",
					marker=dict(size=4, color="red"),
				),
				go.Scatter3d(
					name="Density",
					x=[], y=[], z=[],
					mode="lines",
					line=dict(color="#212121", width=0.5),
					showlegend=True,
					
				),
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

		self.fig.update_layout(legend=dict(
			yanchor="top",
			y=0.99,
			xanchor="right",
			x=0.0
		))

		self._register_callbacks()

	
	def _register_callbacks(self):


		# updates wich sampling methods are available once distribution is selected
		@callback(
			Output(f"sampling-selector-{self.id}", "options"),
			Output(f"sampling-selector-{self.id}", "value"),
			Input("distribution-selector", "value"),
		)
		def update_sampling_methods(selected_distribution):
			options = list(self.object.distributions[selected_distribution].sampling_method_dict.keys())

			# set safe initial value
			initial_value = options[0] 
			return options, initial_value

		# updates the options (silders, etc) for the selected distribution and sampling method
		@callback(
			Output(f"distribution-options-{self.id}", "children"),
			Output(f"sampling-options-{self.id}", "children"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value")
		)
		def update_curr_distribution(selected_distribution, selected_sampling):
			# ids are given in the same order as options_dist and options_sampling
			options_dist = self.object.distributions[selected_distribution].distribution_options
			options_dist_dcc = [opt.to_dash_component("dist", id) for id, opt in enumerate(options_dist)]

			options_sampling = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling]
			options_sampling_dcc = [opt.to_dash_component("sampling", id) for id, opt in enumerate(options_sampling.sample_options)]
			return options_dist_dcc, options_sampling_dcc


		# updates the plot based on selected sampling options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			Input({"type": "dist", "index": ALL}, "value"),
			State({"type": "dist", "index": ALL}, "id"),
			Input({"type": "sampling", "index": ALL}, "value"),
			State({"type": "sampling", "index": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_sample(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _):
			try:
				dist_options =  self.object.distributions[selected_distribution].distribution_options
				sampling_options = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling].sample_options
			except KeyError:
				# got stale values, ignore
				return dash.no_update
			
			# the order of options might not be guaranteed, so we map them by their ids
			id_value_dist = [(id,v) for id, v in zip(ids_dist, values_dist)]
			id_value_samp = [(id,v) for id, v in zip(ids_samp, values_samp)]
			

			# and them sort them, so they are in the same order as sampling_options and dist_options
			options_samp_new = sorted(id_value_samp, key=lambda x: int(x[0]["index"]))
			options_dist_new = sorted(id_value_dist, key=lambda x: int(x[0]["index"]))


			for opt, (id, new_state) in zip(sampling_options, options_samp_new):
				opt.update_state(new_state)

			for opt, (id, new_state) in zip(dist_options, options_dist_new):
				opt.update_state(new_state)

			# samples 
			self.object.update_sample(selected_distribution, selected_sampling, sampling_options, dist_options)


			patched_figure = Patch()


			patched_figure["data"][1].x = self.object.samples[:, 0]
			patched_figure["data"][1].y = self.object.samples[:, 1]
			patched_figure["data"][1].z = self.object.samples[:, 2]

			return patched_figure
		
	# updates the plot based on selected distribution options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			Input({"type": "dist", "index": ALL}, "value"),
			State({"type": "dist", "index": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_dist(values_dist, ids_dist, selected_distribution, selected_sampling, _):
			dist_options =  self.object.distributions[selected_distribution].distribution_options

			# the order of options might not be guaranteed, so we map them by their ids
			# and them sort them, so they are in the same order as sampling_options and dist_options
			id_value_dist = [(id,v) for id, v in zip(ids_dist, values_dist)]
			options_dist_new = sorted(id_value_dist, key=lambda x: int(x[0]["index"]))


			for opt, (id, new_state) in zip(dist_options, options_dist_new):
				opt.update_state(new_state)


			# meshed density function plot plot
			patched_figure = Patch()

			
			pdf = self.object.distributions[selected_distribution].get_pdf(list(dist_options))
			if pdf is not None:
				x, y, z  = self.object.generate_mesh(pdf)
			else:
				x, y, z = [], [], []

			patched_figure["data"][2].x = x
			patched_figure["data"][2].y = y
			patched_figure["data"][2].z = z

			return patched_figure
		
		
		
		
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

		graph = [dcc.Graph(id=f"graph-{self.id}", figure=self.fig)]

		return options, graph