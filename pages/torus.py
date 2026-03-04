import plotly
import dash
from dash import html, dcc, callback, Input, Output, ALL
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from components.split_pane import SplitPane
from model.torus.torus import Torus
from renderer.object_3D_and_2D_renderer import Object3DAnd2DRenderer


dash.register_page(__name__)

torus = Torus()

renderer = Object3DAnd2DRenderer(torus, "torus")
options, graph = renderer.get_layout_components()

layout = SplitPane(
	[
		*options
	],
	[
		*graph
	],
	30

)