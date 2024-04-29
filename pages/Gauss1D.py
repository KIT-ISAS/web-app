import plotly
import dash
from dash import dcc, html, Input, Output, callback, Patch
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, vstack, pi, nan, full, exp, square, sort, arange, array
from numpy.random import randn, randint
from scipy.special import erfinv

dash.register_page(__name__)

methods = ['iid', 'Golden-Sequence', 'Equidistant', 'Unscented']

layout = dbc.Container(
    dbc.Col([
        # Description
        dcc.Markdown(
            '''
            ## 1D Gaussian
            Interactive visualizaton of the univariate Gaussian density

            $$
            f(x) = \\frac{1}{\\sqrt{2\\pi}\\sigma}
            \\cdot \\exp\\!\\left\\{ -\\frac{1}{2} \\cdot \\left(\\frac{x-\\mu}{\\sigma}\\right)^2 \\right\\}\\enspace, \\quad x\\in \\mathbb{R} \\enspace,
            $$

            with mean $\\mu \\in \\mathbb{R}$ and standard deviation $\\sigma \\in \\mathbb{R}_+$ .

            It was discovered by Karl Friedrich Gauß (1777-1855) in Göttingen, Germany.

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

        # Plot
        dcc.Graph(id="gauss1D-graph"),

        # Sampling Strategy RadioItems
        dbc.RadioItems(id='gauss1D-smethod',
                       options=[{"label": x, "value": x} for x in methods],
                       value=methods[randint(len(methods))],
                       inline=True),

        html.P(),  # style={"margin-bottom": "3cm"}

        # param Slider
        dcc.Slider(id="gauss1D-p", min=0, max=1, value=randint(3, 7)/10,
                   tooltip={"template": "p={value}", "placement": "bottom", "always_visible": True}, updatemode='drag', marks=None),

        # L Slider
        dcc.Slider(id="gauss1D-L", min=0, max=100, step=1, value=randint(5, 25),
                   tooltip={"template": "L={value}", "placement": "bottom", "always_visible": True}, updatemode='drag', marks=None),

        # μ Slider
        dcc.Slider(id="gauss1D-μ", min=-5, max=5, step=0.01, value=randint(-20, 20)/10,
                   tooltip={"template": "µ={value}", "placement": "bottom", "always_visible": True}, updatemode='drag', marks=None),

        # σ Slider
        dcc.Slider(id="gauss1D-σ", min=0, max=5, step=0.01, value=randint(5, 20)/10,
                   tooltip={"template": 'σ={value}', "placement": "bottom", "always_visible": True}, updatemode='drag', marks=None),

    ]), fluid=True, className="g-0")


col_density = plotly.colors.qualitative.Plotly[1]
col_samples = plotly.colors.qualitative.Plotly[0]
rang = [-5, 5]


@callback(
    Output('gauss1D-p', 'min'),
    Output('gauss1D-p', 'max'),
    Output('gauss1D-p', 'value'),
    Output('gauss1D-p', 'step'),
    Output('gauss1D-p', 'tooltip'),
    Input("gauss1D-smethod", "value"),
)
def update_smethod(smethod):
    patched_tooltip = Patch()
    match smethod:
        case 'iid':
            patched_tooltip.template = "dice"
            return 0, 1, .5, 0.001, patched_tooltip
        case 'Golden-Sequence':
            patched_tooltip.template = "z={value}"
            return -50, 50, 0, 1, patched_tooltip
        case 'Equidistant':
            patched_tooltip.template = "γ={value}"
            return -1, 1, 0, 0.001, patched_tooltip
        case 'Unscented':
            patched_tooltip.template = "{value}"
            return 0, 2, 1, 0.001, patched_tooltip
        case _:
            raise Exception("Wrong smethod")


@callback(
    Output("gauss1D-graph", "figure"),
    Input("gauss1D-smethod", "value"),
    Input("gauss1D-p", "value"),
    Input("gauss1D-L", "value"),
    Input("gauss1D-μ", "value"),
    Input("gauss1D-σ", "value"),
)
def update(smethod, p, L, μ, σ):
    fig = go.Figure()
    if σ == 0:
        # Dirac Delta
        fig.add_trace(go.Scatter(x=[rang[0], μ, μ, μ, rang[1]], y=[0, 0, 1, 0, 0], hoverinfo='skip', line={'width': 5}, name='Dirac Delta', marker_color=col_density, showlegend=True))
        if L > 0:
            fig.add_trace(go.Scatter(x=[μ, μ], y=[0, 1], name='Samples', mode='lines', marker_color=col_samples, showlegend=True))
    else:
        # Draw Samples
        x = None
        match smethod:
            case 'iid':
                # xUni = sort(rand(L))
                x = sort(randn(L)*σ + μ)
            case 'Golden-Sequence':
                xUni = (sqrt(5)-1)/2 * (arange(L)+1+round(p)) % 1
            case 'Equidistant':
                xUni = (2*arange(L)+1+p)/(2*L)
            case 'Unscented':
                if L == 0:
                    x = array([])
                if L == 1:
                    x = array([μ])
                else:
                    # TODO scaled unscented etc
                    x = array([μ-σ, μ+σ])
            case _:
                raise Exception("Wrong smethod")
        # Transform Samples
        if x is None:
            x = σ*sqrt(2)*erfinv(2*xUni-1) + μ
        L2 = len(x)
        sample_height = full([1, L2], gauss1(0, 0, σ))
        # sample_height = full([1, L], 1/L)
        # Plot Density
        s = linspace(rang[0], rang[1], 500)
        # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
        # TODO lighter fillcolor: fillcolor=matplotlib.colors.to_rgba('#aabbcc80')
        fig.add_trace(go.Scatter(x=s, y=gauss1(s, μ, σ), hoverinfo='skip', line={'width': 5}, line_shape='spline', name='Density', fill='tozeroy', marker_color=col_density, showlegend=True))
        # Plot Samples
        xp = vstack((x, x, full([1, L2], nan))).T.flatten()
        yp = vstack((full([1, L2], 0), sample_height, full([1, L2], nan))).T.flatten()
        fig.add_trace(go.Scatter(x=xp, y=yp, name='Samples', mode='lines', marker_color=col_samples, showlegend=True))
    # Style
    fig.update_xaxes(range=rang, tickmode='array', tickvals=list(range(-5, 6)))
    fig.update_yaxes(range=[0, None])
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    # fig.update_layout(transition_duration=100, transition_easing='linear')
    return fig


def gauss1(x, μ, σ):
    return 1/sqrt(2*pi*σ) * exp(-1/2 * square((x-μ)/σ))
