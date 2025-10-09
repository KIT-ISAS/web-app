from dash import html
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc



def SplitPane(children1, children2):
	return html.Div([
		PanelGroup(
			id='panel-group',
			children=[
				Panel(
					id='left-sidebar',
					minSizePercentage=15,
					children=[
						html.Div([
							dbc.Container(children1, fluid=True)
						], className="bg-light vh-100 w-100 rounded-3") 
					],
				),
				PanelResizeHandle(
					id='resize-handle',
					style={
						"flex": "0 0 20px",
						"margin": "0 -10px",
						"background": "transparent",
						"cursor": "col-resize",
						"userSelect": "none",
						"position": "relative",
						"zIndex": 2,
					},
				),
				Panel(
					id='plot-panel',
					minSizePercentage=15,
					children=[
						dbc.Container(children2, fluid=True)
					],
				)
			], 
			direction='horizontal',
			className='vh-100 w-100 px-0',
		)
	], 
	className='vh-100 px-0',
	)