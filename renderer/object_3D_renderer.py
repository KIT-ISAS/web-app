from functools import lru_cache
from dash import html, dcc, callback, Input, Output, ALL, State, Patch, clientside_callback, ClientsideFunction, MATCH, no_update
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash

from renderer.renderer import Renderer
class Object3DRenderer(Renderer):
	def __init__(self, object_3D, id, register_3d_callbacks=True):
		# dash doesnt like duplicate calback functions
		# so each renderer instance gets a uuid for suffixing
		self.id = id
		self.device_pixel_ratio = 1.0

		# objects should have atleast one corresponding distribution
		self.object = object_3D

		self.x, self.y, self.z = self.object.xyz
	

		# inital figure
		self.config = {
			'responsive': True,
			'scrollZoom': True,
			"modeBarButtonsToRemove": ["select2d", "lasso2d"],
			"toImageButtonOptions": {
				"format": "jpeg",
				"scale": 8,
			}
		}
		
		marker_size = 4 # initial size, will be updated based on samples

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
					x=[],
					y=[],
					z=[],
					mode="markers",
					marker=dict(
						size=marker_size,
						color="red",
						line=dict(width=1, color="black")
					),
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
			margin=dict(l=0, r=0, t=0, b=0),
			# keep camera/zoom/pan while data is patched
			uirevision=f"object-3d-{self.id}",
		)

		# Keep legend overlayed in the corner so it does not steal width from narrow layouts
		self.fig.update_layout(legend=dict(
			yanchor="top",
			y=0.98,
			xanchor="left",
			x=0.02,
			bgcolor="rgba(255,255,255,0.7)"
		))

		if (self.object.camera_settings_3d is not None):
			self.fig.update_layout(scene=dict(camera=self.object.camera_settings_3d))

		self._register_callbacks()
		if register_3d_callbacks:
			self._register_3d_plot_callbacks()

	
	def _register_callbacks(self):

		# gets device pixel ratio from scaling of samples
		clientside_callback(
			ClientsideFunction(namespace="utils", function_name="getDevicePixelRatio"),
			Output(f"device-pixel-ratio-{self.id}", "data"),
			Input(f"graph-{self.id}", "figure"),
		)

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
		# also updates the info markdowns and their hr lines
		@callback(
			Output(f"distribution-options-{self.id}", "children"),
			Output(f"sampling-options-{self.id}", "children"),
			Output(f"distribution-info-markdown-{self.id}", "children"),
			Output(f"sampling-method-info-markdown-{self.id}", "children"),
			Output(f"distribution-info-divider-{self.id}", "hidden"),
			Output(f"sampling-method-info-divider-{self.id}", "hidden"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value")
		)
		def update_curr_distribution(selected_distribution, selected_sampling):
			# ids are given in the same order as options_dist and options_sampling
			options_dist = self.object.distributions[selected_distribution].distribution_options
			options_dist_dcc = [opt.to_dash_component("dist", id, self.id) for id, opt in enumerate(options_dist)]

			options_sampling = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling]
			options_sampling_dcc = [opt.to_dash_component("sampling", id, self.id) for id, opt in enumerate(options_sampling.sample_options)]

			dist_info_md = self.object.distributions[selected_distribution].info_md
			sampling_info_md = options_sampling.info_md

			dist_hidden = dist_info_md is None or dist_info_md.strip() == ""
			sampling_hidden = sampling_info_md is None or sampling_info_md.strip() == ""


			return options_dist_dcc, options_sampling_dcc, dist_info_md, sampling_info_md, dist_hidden, sampling_hidden


		# optional manual input
		@callback(
			Output({"type": "sampling", "renderer": self.id, "index": MATCH, "manual": True}, "value"),
			Output({"type": "manual_input-sampling", "renderer": self.id, "index": MATCH}, "value"),
			Input({"type": "manual_input-sampling", "renderer": self.id, "index": MATCH}, "value"),
			Input({"type": "sampling", "renderer": self.id, "index": MATCH, "manual": True}, "value"),
			State("distribution-selector", "value"),
			State(f"sampling-selector-{self.id}", "value"),
			prevent_initial_call=True,
		)
		def manual_input_changed(val, val_silder, selected_distribution, selected_sampling):
			triggered_id = dash.ctx.triggered_id
			source = triggered_id["type"]

			if val is None and source == "manual_input-sampling":
				return no_update, no_update

			sampling_options = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling].sample_options

			try:
				index = int(triggered_id["index"])
			except (TypeError, ValueError):
				return no_update, no_update
			if index < 0 or index >= len(sampling_options):
				return no_update, no_update

			wrapper = sampling_options[index]
			
			if source == "manual_input-sampling": # manual input changed, update slider

				if (wrapper.check_input is None or wrapper.check_input(val)) and wrapper.slider.is_valid(val):
					slider_value = wrapper.update_state_manual(val)
					return slider_value, no_update
				else:
					return no_update, no_update
				
			else: # slider changed, update manual input
				return no_update, wrapper.slider.transfrom_up(val_silder)

		@callback(
			Output({"type": "dist", "renderer": self.id, "index": MATCH, "manual": True}, "value"),
			Output({"type": "manual_input-dist", "renderer": self.id, "index": MATCH}, "value"),
			Input({"type": "manual_input-dist", "renderer": self.id, "index": MATCH}, "value"),
			Input({"type": "dist", "renderer": self.id, "index": MATCH, "manual": True}, "value"),
			State("distribution-selector", "value"),
			State(f"sampling-selector-{self.id}", "value"),
			prevent_initial_call=True,
		)
		def manual_input_dist_changed(val_manual, val_slider, selected_distribution, selected_sampling):
			triggered_id = dash.ctx.triggered_id
			source = triggered_id["type"]

			if val_manual is None and source == "manual_input-dist":
				return no_update, no_update

			dist_options =  self.object.distributions[selected_distribution].distribution_options

			try:
				index = int(triggered_id["index"])
			except (TypeError, ValueError):
				return no_update, no_update
			if index < 0 or index >= len(dist_options):
				return no_update, no_update

			wrapper = dist_options[index]

			if source == "manual_input-dist":
				# check_input is given by distribution/ sampling method, if None, no special constraints are given
				# slider.is_valid is given by the slider itself, can be less strict
				if (wrapper.check_input is None or wrapper.check_input(val_manual)) and wrapper.slider.is_valid(val_manual):
					slider_value = wrapper.update_state_manual(val_manual)
					return slider_value, no_update
				return no_update, no_update

			# slider changed, sync manual input display
			return no_update, wrapper.slider.transfrom_up(val_slider)

	def _register_3d_plot_callbacks(self):

		# updates the plot based on selected sampling options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			Input({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "value"),
			State({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "id"),
			Input({"type": "sampling", "renderer": self.id, "index": ALL, "manual": ALL}, "value"),
			State({"type": "sampling", "renderer": self.id, "index": ALL, "manual": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			State(f"device-pixel-ratio-{self.id}", "data"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_sample_callback(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr):
			return self.update_plot_sample(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr)
		
		# updates the plot based on selected distribution options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			Input({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "value"),
			State({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "id"),
			Input("distribution-selector", "value"),
			Input(f"sampling-selector-{self.id}", "value"),
			Input(f"distribution-options-{self.id}", "children"),
			prevent_initial_call='initial_duplicate'
		)
		def update_plot_dist_callback(values_dist, ids_dist, selected_distribution, selected_sampling, _):
			return self.update_plot_dist(values_dist, ids_dist, selected_distribution, selected_sampling, _)

		
		
	def update_plot_sample(self, values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr):
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
		samples, _ = self.object.update_sample(selected_distribution, selected_sampling, sampling_options, dist_options)


		patched_figure = Patch()


		patched_figure["data"][1].x = samples[:, 0]
		patched_figure["data"][1].y = samples[:, 1]
		patched_figure["data"][1].z = samples[:, 2]

		# set size based on number of samples
		if samples.size == 0:
			marker_size = 0 
		else:
			sample_count = samples.shape[0]
			marker_size = (10 * (sample_count / 100) ** (-0.35)) / dpr
			marker_size = np.minimum(10,marker_size) 
		

		patched_figure["data"][1].marker.size = marker_size	
		return patched_figure
	
	def update_plot_dist(self, values_dist, ids_dist, selected_distribution, selected_sampling, _):
		dist_options =  self.object.distributions[selected_distribution].distribution_options

		# the order of options might not be guaranteed, so we map them by their ids
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
			dcc.Store(id=f"device-pixel-ratio-{self.id}", data=1),
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

			html.Hr(id=f"distribution-info-divider-{self.id}", hidden=True),

			dcc.Markdown(id=f"distribution-info-markdown-{self.id}", mathjax=True), 

			html.Hr(id=f"sampling-method-info-divider-{self.id}", hidden=True),

			dcc.Markdown(id=f"sampling-method-info-markdown-{self.id}", mathjax=True),


		]

		graph = [dcc.Graph(id=f"graph-{self.id}", figure=self.fig, config=self.config, style={'height': '100%'})]

		return options, graph
