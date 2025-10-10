import plotly
import dash
from dash import html, dcc
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from components.split_pane import SplitPane
from model.sphere.sphere import Sphere

dash.register_page(__name__)

sphere = Sphere()
x, y, z = sphere.xyz
sphere.samples = np.array([
	[0,0,1],
	[0,1,0],
	[1,0,0]
])


fig = go.Figure(
	data=[
		go.Surface(
			x=x, y=y, z=z,
			showscale=False
		),
		go.Scatter3d(
			x=sphere.samples[:][0], y=sphere.samples[:][1], z=sphere.samples[:][2],
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

layout = SplitPane(
	[
		html.P("this is where the controls will go")
	],
	[
		dcc.Graph(figure=fig)
	],
	30

)