import dash
import flask
from dash import Dash, html
import dash_bootstrap_components as dbc

# Usage Locally:
# $ python app.py

# select theme
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
external_stylesheets = [dbc.themes.CERULEAN]  # CERULEAN, DARKLY, PULSE

server = flask.Flask(__name__)

app = Dash(__name__, external_stylesheets=external_stylesheets, server=server, use_pages=True)  # , suppress_callback_exceptions=True

app.layout = dbc.Container([
    html.H1('ISAS Interactive'),
    dbc.Nav([
        dbc.NavLink(html.Div(f"{page['name']}"), href=page["relative_path"], active="exact")
        for page in dash.page_registry.values()
    ], pills=True, className='bg-light'),
    html.P(),
    dash.page_container
], fluid=True)

if __name__ == '__main__':
    # processes=6, threaded=False,
    # app.run(debug=True, threaded=True, host='0.0.0.0', port='8080')
    app.run(debug=True, processes=6, threaded=False, host='0.0.0.0', port='8080')
    # app.run(debug=True)
