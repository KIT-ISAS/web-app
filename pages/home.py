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

        Code: https://github.com/KIT-ISAS/web-app

        Version History:
        - 2024-04 | Daniel Frisch | gauss1d, gauss2d
        '''
        )
], fluid=True, className="g-0")
