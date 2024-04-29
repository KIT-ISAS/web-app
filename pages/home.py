import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dcc.Markdown(
        '''
        Responsive visualization of probability densities, samples, and filtering methods.
        Parameters can be interactively modified using sliders.
        Used in our lectures and for research.
        Created with Plotly Dash.
        '''
        )
], fluid=True, className="g-0")
