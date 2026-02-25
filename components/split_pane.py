from dash import html
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
import dash_bootstrap_components as dbc



def SplitPane(children1, children2, default_size):
	return html.Div([
		PanelGroup(
			id='panel-group',
			children=[
				Panel(
					id='left-sidebar',
					className="split-pane-left",
					minSizePercentage=15,
					defaultSizePercentage=default_size,
					children=[
						html.Div(
							children1,
							className="bg-light h-100 w-100 rounded-3 p-3 pb-5", style={'overflowY': 'scroll', 'overflowX': 'hidden', 'minHeight': '0'},
							)
					],
				),
				PanelResizeHandle(
					id='resize-handle',
					className="split-pane-handle",
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
					className="split-pane-right",
					minSizePercentage=15,
					children=children2,
				)
			], 
			direction='horizontal',
			className='split-pane-group w-100 px-0 pb-2',
			style={'minHeight': '0'}
		)
	], 
	className='px-0 flex-grow-1 d-flex flex-column',
	id='pangelgroup-parent-container',
	style={'minHeight': '0'}
	)