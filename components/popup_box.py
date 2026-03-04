import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, callback, State

def PopupBox(id, label, title, children):
	@callback(
		Output(f"modal-{label}-{id}", "is_open"),
		Input(f"popup-box-{label}-{id}", "n_clicks"),
		Input(f"close-{label}-{id}", "n_clicks"),
		State(f"modal-{label}-{id}", "is_open"),
	)
	def toggle_modal(n1, n2, is_open):
		if n1 or n2:
			return not is_open
		return is_open


	button = html.Div(
		children=[
			dbc.Button(label, id=f"popup-box-{label}-{id}", n_clicks=0)
		],
		style={
			"caretColor": "transparent",
			"userSelect": "none"
		}
	)

	modal = dbc.Modal(
		id=f"modal-{label}-{id}",
		is_open=False,
		children=[
			html.Div(
				children=[dbc.ModalHeader(dbc.ModalTitle(title), close_button=True)],
				style={
					"caretColor": "transparent",
					"userSelect": "none"
				}
			),
			dbc.ModalBody(children),
			dbc.ModalFooter(
                    dbc.Button("Close", id=f"close-{label}-{id}", n_clicks=0)
            ),
		],
		size="xl",
		centered=True,
		scrollable=True,
	)
	return button, modal

