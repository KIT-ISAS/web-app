from dash import html, dcc, callback, Input, Output, ALL
import plotly.graph_objects as go
import uuid

class Object3DRenderer:
	def __init__(self, object_3D):
		# dash doesnt like duplicate calback functions
		# so each renderer instance gets a uuid for suffixing
		self.uuid = str(uuid.uuid4()) 

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

		@callback(
			Output(f"distribution-options-{self.uuid}", "children"),
			Input("distribution-selector", "value"),
		)
		def update_curr_distribution(selected_distribution):
			options = self.object.distributions[selected_distribution].sample_options

			options_dcc = [opt.to_dash_component(f"id") for id, opt in enumerate(options)]
			return options_dcc

		@callback(
			Output(f"graph-{self.uuid}", "figure"),
			Input({"type": "dynamic-option", "index": ALL}, "value"),
			Input("distribution-selector", "value"),
			Input(f"distribution-options-{self.uuid}", "children"),
		)
		def update_plot(options, selected_distribution, _):
			dist_options =  self.object.distributions[selected_distribution].sample_options
			for opt, new_state in zip(dist_options, options):
				opt.update_state(new_state)

			self.object.update_sample(selected_distribution, dist_options)

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
		options = [
			html.Br(),
			html.P("Select Distribution:"),
			dcc.RadioItems(
				id="distribution-selector",
				options=(list(self.object.distributions.keys())),
				value=self.object.distributions[list(self.object.distributions.keys())[0]].get_name(),
			),
			html.Br(),
			html.Hr(),
			html.Br(),

			html.Div(id=f"distribution-options-{self.uuid}"),
		]

		graph = [dcc.Graph(id=f"graph-{self.uuid}", figure=self.fig)]

		return options, graph