import plotly
import dash
from dash import html
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import dash_vtk
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



layout = SplitPane(
	[
		html.P("this is where the controls will go")
	],
	[
		dash_vtk.View(
		children=[
			dash_vtk.GeometryRepresentation(
				property={"color": [0.8, 0.8, 0.8]},
				children=[
					dash_vtk.Algorithm(
						vtkClass="vtkSphereSource",
						state={
							"phiResolution": 32,
							"thetaResolution": 32,
							"radius": 1.0,
						},
					)
				]
			),
			dash_vtk.GeometryRepresentation(
			mapper={"scalarVisibility": False},
			property={"color": [1, 0, 0], "pointSize": 6},
			children=[
				dash_vtk.PolyData(
					points=sphere.samples.ravel(),
					# verts is an array like [1, 0, 1, 1, 1, 2, ...]
					verts=np.c_[np.ones(sphere.samples.shape[0], dtype=np.int64), np.arange(sphere.samples.shape[0])].ravel().tolist(),
				)
			],
		),
		],
		background=[1, 1, 1],
		style={"height": "100vh", "width": "100%"},
	)
	],
	30

)