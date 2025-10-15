import plotly
import dash
from dash import html, dcc, callback, Input, Output, ALL
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from components.split_pane import SplitPane
from model.torus.torus import Torus
from renderer.Object3DRenderer import Object3DRenderer


dash.register_page(__name__)

torus = Torus()

renderer = Object3DRenderer(torus)
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