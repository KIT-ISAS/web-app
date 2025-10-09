import plotly
import dash
from dash import html
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc

from components.split_pane import SplitPane

dash.register_page(__name__)


layout = SplitPane(
	[
		html.P("this is where the controls will go")
	],
	[
		html.P("this is where the plot will go")
	]

)