from dash import html

# wrapps component in a label
def Label(label, component):
	return html.Div([
				html.Label(label),
				component,
			])