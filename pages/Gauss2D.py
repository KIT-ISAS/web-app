import plotly
import dash
import pandas
from urllib.error import HTTPError
from dash import dcc, html, Input, Output, callback, Patch
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, vstack, pi, nan, full, exp, square, arange, array, sin, cos, diff, matmul, log10, deg2rad
from numpy.random import randn, randint
from numpy.linalg import cholesky, eig
from scipy.special import erfinv

dash.register_page(__name__)


# Samples Library
data_dict = {}


# Get Samples from Library (and load if not available)
def get_data(url):
    if not (url in data_dict):
        try:
            data = pandas.read_csv(url, header=None).to_numpy()
        except HTTPError:
            # URL doesn't exist
            data = full([2, 0], nan)
        data_dict[url] = data
    return data_dict[url]


def url_SND_LCD(D, L):
    return f'https://raw.githubusercontent.com/KIT-ISAS/deterministic-samples-csv/main/standard-normal/glcd/D{D}-N{L}.csv'


# Define Parameters
# Sampling methods
smethods = ['iid', 'Fibonacci', 'LCD']  # , 'Unscented'
# Transformation methods
tmethods = ['Cholesky', 'Eigendecomposition']
# Colors
col_density = plotly.colors.qualitative.Plotly[1]
col_samples = plotly.colors.qualitative.Plotly[0]
# axis limits
rangx = [-5, 5]
rangy = [-4, 4]
# plot size relative to window size
relwidth = 100
relheight = round((relwidth/diff(rangx)*diff(rangy))[0])
# Gauss ellipse
s = linspace(0, 2*pi, 500)
circ = vstack((cos(s), sin(s))) * 2

# Initialize Plot
# https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
fig = go.Figure()
fig.add_trace(go.Scatter(name='Density', x=[0], y=[0], mode='lines',   marker_color=col_density, showlegend=True, hoverinfo='skip', line={'width': 3}, line_shape='spline', fill='tozerox'))
fig.add_trace(go.Scatter(name='Samples', x=[0], y=[0], mode='markers', marker_color=col_samples, showlegend=True))
fig.update_xaxes(range=rangx, tickmode='array', tickvals=list(range(rangx[0], rangx[1]+1)))
fig.update_yaxes(range=rangy, tickmode='array', tickvals=list(range(rangy[0], rangy[1]+1)), scaleanchor="x", scaleratio=1)
fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
# fig.update_layout(transition_duration=100, transition_easing='linear')


layout = dbc.Container(
    dbc.Col([
        # Plot
        dcc.Graph(id="gauss2D-graph", figure=fig, style={'width': f'{relwidth}vw', 'height': f'{relheight}vw'}),

        # Sampling Strategy RadioItems
        dbc.RadioItems(id='gauss2D-smethod',
                       options=[{"label": x, "value": x} for x in smethods],
                       value=smethods[randint(len(smethods))],
                       inline=True),

        # Transformation Method RadioItems
        dbc.RadioItems(id='gauss2D-tmethod',
                       options=[{"label": x, "value": x} for x in tmethods],
                       value=tmethods[randint(len(tmethods))],
                       inline=True),

        html.P(),  # style={"margin-bottom": "3cm"}

        # param Slider
        dcc.Slider(id="gauss2D-p", min=0, max=1, value=randint(3, 7)/10, updatemode='drag', marks=None,
                   tooltip={"template": "p={value}", "placement": "bottom", "always_visible": True}),

        # L Slider
        dcc.Slider(id="gauss2D-L", min=log10(1.2), max=4.001, step=0.001, value=2, updatemode='drag', marks=None,
                   tooltip={"template": "L={value}", "placement": "bottom", "always_visible": True, "transform": "trafo_L"}),

        # σ Slider
        dcc.Slider(id="gauss2D-σx", min=0, max=5, step=0.01, value=1, updatemode='drag', marks=None,
                   tooltip={"template": 'σx={value}', "placement": "bottom", "always_visible": True}),
        dcc.Slider(id="gauss2D-σy", min=0, max=5, step=0.01, value=1, updatemode='drag', marks=None,
                   tooltip={"template": 'σy={value}', "placement": "bottom", "always_visible": True}),

        # ρ Slider
        dcc.Slider(id="gauss2D-ρ", min=-1, max=1, step=0.001, value=0, updatemode='drag', marks=None,
                   tooltip={"template": 'ρ={value}', "placement": "bottom", "always_visible": True}),

        # Description
        dcc.Markdown(
            '''
            ## 2D Gaussian
            Interactive visualizaton of the bivariate Gaussian density

            $$
            f(\\underline x) = \\frac{1}{2\\pi \\sqrt{\\det(\\textbf{C})}}
            \\cdot \\exp\\!\\left\\{ -\\frac{1}{2}
            \\cdot (\\underline x - \\underline \\mu)^\\top \\textbf{C}^{-1} (\\underline x - \\underline \\mu) \\right\\} \\enspace, \\quad \\underline{x}\\in \\mathbb{R}^2 \\enspace.
            $$

            ### Formulas
            - quantile function \n
              $Q(p) = \\mu + \\sigma\\, \\sqrt{2}\\, \\text{erf}^{-1}(2p-1)$
            - uniform to Gaussian samples \n
              $x_i^{\\text{Gauss}} = Q(x_i^{\\text{uni}})$
            - golden Kronecker sequence  \n
              $x_i^{\\text{uni}}=\\mod( \\Phi \\cdot (i+z), 1) \\enspace, \\quad i \\in \\{1,2,\\ldots,L\\}\\enspace, \\quad z \\in \\mathbb{Z}$
            - equidistant samples \n
              $x_i^{\\text{uni}} = \\frac{2 i - 1 + \\gamma}{2 L} \\enspace, \\quad i \\in \\{1,2,\\ldots,L\\}\\enspace,\\quad \\gamma\\in[-1,1]$
            - unscented (𝐿=2)\n
              $x_1=\\mu-\\sigma\\enspace, \\quad x_2=\\mu+\\sigma$
            - unscented (𝐿=3) \n
              TODO

            ### Interactivity
            - sampling methods
                - independent identically distributed (iid), the usual random samples
                - golden sequence, a low-discrepancy Kronecker sequence based on the golden ratio,
                - equidistant, with identical amount of probability mass for all samples
                - unscented transform sampling (𝐿=2)
            - sampling parameter
                - iid: dice again
                - golden: integer offset 𝑧
                - equidistant: offset 𝛾
                - unscented: TODO
            - number of Samples 𝐿
            - density parameters
                - mean 𝜇
                - standard deviation 𝜎
            ''',
            mathjax=True),
    ]), fluid=True, className="g-0")


@callback(
    Output('gauss2D-p', 'min'),
    Output('gauss2D-p', 'max'),
    Output('gauss2D-p', 'value'),
    Output('gauss2D-p', 'step'),
    Output('gauss2D-p', 'tooltip'),
    Input("gauss2D-smethod", "value"),
)
def update_smethod(smethod):
    patched_tooltip = Patch()
    match smethod:
        case 'iid':
            patched_tooltip.template = "dice"
            # min, max, value, step, tooltip
            return 0, 1, .5, 0.001, patched_tooltip
        case 'Fibonacci':
            patched_tooltip.template = "z={value}"
            return -50, 50, 0, 1, patched_tooltip
        case 'LCD':
            patched_tooltip.template = "α={value}°"
            return -360, 360, 0, 0.1, patched_tooltip
        case 'Unscented':
            patched_tooltip.template = "{value}"
            return 0, 2, 1, 0.001, patched_tooltip
        case _:
            raise Exception("Wrong smethod")


@callback(
    Output("gauss2D-graph", "figure"),
    Input("gauss2D-smethod", "value"),
    Input("gauss2D-tmethod", "value"),
    Input("gauss2D-p", "value"),
    Input("gauss2D-L", "value"),
    Input("gauss2D-σx", "value"),
    Input("gauss2D-σy", "value"),
    Input("gauss2D-ρ", "value"),
)
def update(smethod, tmethod, p, L0, σx, σy, ρ):
    # Slider Transform,
    L = trafo_L(L0)
    # Mean
    # μ = array([[μx], [μy]])
    μ = array([[0], [0]])
    # Covariance
    C = array([[square(σx), σx*σy*ρ], [σx*σy*ρ, square(σy)]])
    C_D, C_R = eig(C)
    C_D = C_D[..., None]  # to column vector

    patched_fig = Patch()
    # Draw SND
    match smethod:
        case 'iid':
            xySND = randn(2, L)
        case 'Fibonacci':
            xUni = (sqrt(5)-1)/2 * (arange(L)+1+round(p)) % 1
            yUni = (2*arange(L)+1)/(2*L)  # +p
            xyUni = vstack((xUni, yUni))
            xySND = sqrt(2)*erfinv(2*xyUni-1)
        case 'LCD':
            xySND = get_data(url_SND_LCD(2, L))
            xySND = matmul(rot(p), xySND)
        # case 'Unscented':
        #     if L == 0:
        #         x = array([])
        #     elif L == 1:
        #         x = array([μx])
        #     elif L == 2:
        #         # TODO scaled unscented etc
        #         x = array([μx-σx, μx+σx])
        #     else:
        #         x = full([2,0], nan)
        case _:
            raise Exception("Wrong smethod")
    match tmethod:
        case 'Cholesky':
            xyG = matmul(cholesky(C), xySND) + μ
        case 'Eigendecomposition':
            xyG = matmul(C_R, sqrt(C_D) * xySND) + μ
        case _:
            raise Exception("Wrong smethod")
    # Plot Samples
    patched_fig['data'][1]['x'] = xyG[0, :]
    patched_fig['data'][1]['y'] = xyG[1, :]
    # Plot Ellipse
    elp = matmul(C_R * sqrt(C_D).T, circ) + μ
    patched_fig['data'][0]['x'] = elp[0, :]
    patched_fig['data'][0]['y'] = elp[1, :]
    return patched_fig


def gauss1(x, μ, σ):
    return 1/sqrt(2*pi*σ) * exp(-1/2 * square((x-μ)/σ))


# Slider Transform, must be idencital to window.dccFunctions.trafo_L in assets/tooltip.js
def trafo_L(L0):
    if L0 < log10(1.25):
        return 0
    else:
        return round(10 ** L0)


def rot(a):
    ar = deg2rad(a)
    return array([[cos(ar), -sin(ar)], [sin(ar), cos(ar)]])
