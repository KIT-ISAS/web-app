import plotly
import dash
from dash import html, dcc, callback, Input, Output, ALL
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from components.split_pane import SplitPane
from model.torus.torus import Torus

dash.register_page(__name__)

torus = Torus()
x, y, z = torus.xyz


fig = go.Figure(
	data=[
		go.Surface(
			x=x, y=y, z=z,
			colorscale="Viridis",
			showscale=False
		),
		go.Scatter3d(
			x=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[0] if torus.samples.size else [],
			y=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[1] if torus.samples.size else [],
			z=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[2] if torus.samples.size else [],
			mode="markers",
			marker=dict(size=4, color="red")
		)
	]
)

fig.update_layout(
	scene=dict(
		aspectmode='data',
		xaxis=dict(visible=False),
		yaxis=dict(visible=False),
		zaxis=dict(visible=False),
	),
	margin=dict(l=0, r=0, t=0, b=0)
)

@callback(
	Output("distribution-options-torus", "children"),
	Input("distribution-selector", "value"),
)
def update_curr_distribution(selected_distribution):
	options = torus.distributions[selected_distribution].sample_options

	options_dcc = [opt.to_dash_component(f"id") for id, opt in enumerate(options)]
	return options_dcc

@callback(
	Output("graph-torus", "figure"),
	Input({"type": "dynamic-option", "index": ALL}, "value"),
	Input("distribution-selector", "value"),
	Input("distribution-options-torus", "children"),
)
def update_plot(options, selected_distribution, _):
	dist_options =  torus.distributions[selected_distribution].sample_options
	for opt, new_state in zip(dist_options, options):
		opt.update_state(new_state)

	torus.samples = torus.distributions[selected_distribution].sample(dist_options)
	data =  [
		go.Surface(
			x=x, y=y, z=z,
			showscale=False,
			colorscale="Viridis",
		),
		go.Scatter3d(
			x=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[0] if torus.samples.size else [],
			y=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[1] if torus.samples.size else [],
			z=(Torus.t_p_to_xyz(torus.samples[:, 0], torus.samples[:, 1]))[2] if torus.samples.size else [],
			mode="markers",
			marker=dict(size=4, color="red")
		)
	]
	return go.Figure(data=data, layout=fig.layout)


layout = SplitPane(
	[
		html.Br(),
		html.P("Select Distribution:"),
		dcc.RadioItems(
			id="distribution-selector",
			options=(list(torus.distributions.keys())),
			value=torus.distributions[list(torus.distributions.keys())[0]].get_name(),
		),
		html.Br(),
		html.Hr(),
		html.Br(),

		html.Div(id="distribution-options-torus"),
	],
	[
		dcc.Graph(id="graph-torus", figure=fig)
	],
	30

)