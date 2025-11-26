from dash import html, dcc, callback, Input, Output, ALL, State, Patch, no_update
import numpy as np
import plotly.graph_objects as go

from renderer.Object3DRenderer import Object3DRenderer

class Object3DAnd2DRenderer(Object3DRenderer):
	def __init__(self, object, id):
		# the renderer starts out in 3d mode
		super().__init__(object, id, register_3d_callbacks=False)
		self.register_plot_callbacks()
		self.register_mode_callbacks()

		self.per_x = object.plot_settings_2d.periodic_x
		self.per_y = object.plot_settings_2d.periodic_y

		self.perx_x_amount = object.plot_settings_2d.periodic_x_amount
		self.pery_y_amount = object.plot_settings_2d.periodic_y_amount

		self.reverse_x_y_axis = object.plot_settings_2d.reverse_x_y_axis

		x_min, y_min, x_max, y_max = object.plot_settings_2d.color_location
		self.color_heatmap_x = np.linspace(x_min, x_max, 100)
		self.color_heatmap_y = np.linspace(y_min, y_max, 100)
		self.color_meshgrid = np.meshgrid(self.color_heatmap_x, self.color_heatmap_y, indexing="xy")

		padd = 0.5

		self.fig_2d = go.Figure(
			data=[
				go.Scattergl(
					name="Samples",
					x=[],
					y=[],
					mode="markers",
					marker=dict(
						size=6,
						color="red",
						line=dict(width=1, color="black")
					),
					showlegend=True,
				),
				
				go.Scattergl(
					name="Samples (periodic extension)",
					x=[],
					y=[],
					mode="markers",
					marker=dict(
						size=6,
						color="#a2acbd",
						line=dict(width=1, color="#a2acbd")
					),
					showlegend=(object.plot_settings_2d.periodic_x or object.plot_settings_2d.periodic_y)
				),

				go.Heatmap(
					name="PDF",
					x=self.color_heatmap_x,
					y=self.color_heatmap_y,
					z=np.zeros((100,100)),
					colorscale="Plasma",
					zmin=0.0,
					zmax=1.0,
					zsmooth="best",
					colorbar=dict(title="pdf"),
					showscale=True,
					showlegend=True,
				)
			]
		)
		self.fig_2d.update_layout(legend=dict(
			yanchor="top",
			y=0.99,
			xanchor="left",
			x=0.01,
		))
		self.fig_2d.update_layout(dragmode="pan")

		if object.plot_settings_2d is not None:
			self.fig_2d.update_xaxes(
				title_text=object.plot_settings_2d.x_title,
				tickmode="array",
				tickvals=object.plot_settings_2d.axes_2d_x[0],
				ticktext=object.plot_settings_2d.axes_2d_x[1],
				zeroline=False,
			)
			self.fig_2d.update_yaxes(
				title_text=object.plot_settings_2d.y_title,
				tickmode="array",
				tickvals=object.plot_settings_2d.axes_2d_y[0],
				ticktext=object.plot_settings_2d.axes_2d_y[1],
				zeroline=False,
			)

			if object.plot_settings_2d.lock_aspect_ratio:
				self.fig_2d.update_yaxes(
					scaleanchor = "x",
					scaleratio = 1,
				)

			# so that it doent autoscale for periodicity points
			padd = 0.5
			if self.per_x: 
				self.fig_2d.update_xaxes(
					range=[0 - padd, self.perx_x_amount + padd],
				)
			if self.per_y:
				self.fig_2d.update_yaxes(
					range=[0 - padd, self.pery_y_amount + padd],
				)
		
				

	def register_plot_callbacks(self):
		# updates the plot based on selected sampling options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			State(f"mode-selector-{self.id}", "value"),
			Input(f"mode-done-{self.id}", "data"),
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
		def update_plot_sample_callback(mode, _mode_counter, values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr):
			if mode == "3D View":
				return self.update_plot_sample(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr)
			else:
				return self.update_plot_sample_2d(values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr)
		
		# updates the plot based on selected distribution options
		@callback(
			Output(f"graph-{self.id}", "figure", allow_duplicate=True),
			State(f"mode-selector-{self.id}", "value"),
			Input(f"mode-done-{self.id}", "data"),
			Input({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "value"),
			State({"type": "dist", "renderer": self.id, "index": ALL, "manual": ALL}, "id"),
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

	def update_plot_sample_2d(self, values_dist, ids_dist, values_samp, ids_samp, selected_distribution, selected_sampling, _, dpr):
		try:
			dist_options =  self.object.distributions[selected_distribution].distribution_options
			sampling_options = self.object.distributions[selected_distribution].sampling_method_dict[selected_sampling].sample_options
		except KeyError:
			# got stale values, ignore
			return no_update
		
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
		tp = self.object.samples_2d

		# marker size scaling
		sample_count = self.object.samples.shape[0]
		if sample_count == 0:
			marker_size = 0 # no samples, no size
		else:
			marker_size = (10 * (sample_count / 100) ** (-0.35)) / dpr
			marker_size = np.minimum(10,marker_size)

		patched_figure["data"][0].marker.size = marker_size * 1.5
		patched_figure["data"][1].marker.size = marker_size

		if not self.reverse_x_y_axis:
			# True: (eg torus: x is p, y is t)
			# False: (eg cylinder: x is p, y is z)
			tp[:, [0, 1]] = tp[:, [1, 0]] # swap order, below code assumes self.reverse_x_y_axis is True

		patched_figure["data"][0].x = tp[:, 1]
		patched_figure["data"][0].y = tp[:, 0]
		



		ext_x = np.array([])
		ext_y = np.array([])
		if self.per_x:
			ext_x = np.concatenate([tp[:,1] - self.perx_x_amount, tp[:,1] + self.perx_x_amount])
			ext_y = np.concatenate([tp[:,0], tp[:,0]])
			
		if self.per_y:
			ext_x = np.concatenate([ext_x, tp[:,1], tp[:,1]])
			ext_y = np.concatenate([ext_y, tp[:,0] - self.pery_y_amount, tp[:,0] + self.pery_y_amount])
		
		if self.per_x and self.per_y: # all four corners
			ext_x = np.concatenate([
				ext_x,
				tp[:,1] + self.perx_x_amount,
				tp[:,1] + self.perx_x_amount,
				tp[:,1] - self.perx_x_amount,
				tp[:,1] - self.perx_x_amount
			])

			ext_y = np.concatenate([
				ext_y,
				tp[:,0] + self.pery_y_amount,
				tp[:,0] - self.pery_y_amount,
				tp[:,0] + self.pery_y_amount,
				tp[:,0] - self.pery_y_amount
			])


		if self.per_x or self.per_y:
			patched_figure["data"][1].x = ext_x
			patched_figure["data"][1].y = ext_y

		return patched_figure


	def update_plot_dist_2d(self, values_dist, ids_dist, selected_distribution, selected_sampling, _):
		patched_figure = Patch()
		try:
			dist_options =  self.object.distributions[selected_distribution].distribution_options
		except KeyError:
			# got stale values, ignore
			return no_update
		
		# the order of options might not be guaranteed, so we map them by their ids
		id_value_dist = [(id,v) for id, v in zip(ids_dist, values_dist)]
		

		# and them sort them, so they are in the same order as sampling_options and dist_options
		options_dist_new = sorted(id_value_dist, key=lambda x: int(x[0]["index"]))


		for opt, (id, new_state) in zip(dist_options, options_dist_new):
			opt.update_state(new_state)

		pdf = self.object.distributions[selected_distribution].get_pdf(list(dist_options))

		# pdf heatmap
		X, Y = self.color_meshgrid
		if self.reverse_x_y_axis:
			xy = np.column_stack((Y.ravel(), X.ravel()))
		else:
			xy = np.column_stack((X.ravel(), Y.ravel()))
		z_flat = self.object.pdf_2d(xy, pdf).reshape(X.shape)

		z = z_flat.reshape(X.shape)

		patched_figure["data"][2].z = z

		return patched_figure

	def get_layout_components(self):
		initial_distribution = self.object.distributions[list(self.object.distributions.keys())[0]]
		initial_sampling_method = initial_distribution.sampling_methods[0].get_name() if initial_distribution.sampling_methods else "no sampling methods found"
		initial_sampling_options = [x.get_name() for x in initial_distribution.sampling_methods]
		
		options = [
			dcc.Store(id=f"device-pixel-ratio-{self.id}", data=1),

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

			html.Hr(id=f"distribution-info-divider-{self.id}", hidden=True),

			dcc.Markdown(id=f"distribution-info-markdown-{self.id}", mathjax=True), 

			html.Hr(id=f"sampling-method-info-divider-{self.id}", hidden=True),

			dcc.Markdown(id=f"sampling-method-info-markdown-{self.id}", mathjax=True),

			dcc.Markdown(id=f"sampling-method-info-markdown-{self.id}", mathjax=True),
		]

		graph = [dcc.Graph(id=f"graph-{self.id}", figure=self.fig, config=self.config, style={'height': '100%'})]

		return options, graph
