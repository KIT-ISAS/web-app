import plotly
import dash
from dash import html
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import dash_vtk

from components.split_pane import SplitPane

dash.register_page(__name__)


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
						},
					)
				]
			)
		],
		background=[1, 1, 1],
		style={"height": "100vh", "width": "100%"},
	)
	],
	30

)