import plotly
import dash
import pandas
import math
from util.sampling_test import update_julier
from util.sampling_test import update_mengazz
from urllib.error import HTTPError
from dash import dcc, html, Input, Output, callback, Patch,ctx
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, vstack, hstack, pi, nan, full, exp, square, arange, array, sin, cos, diff, matmul, log10, deg2rad, identity, ones, zeros, diag, cov, mean, atan2
from numpy.random import randn, randint
from numpy.linalg import cholesky, eig, det, inv
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
smethods = ['iid', 'Fibonacci', 'LCD', 'SP-Julier04', 'SP-Menegaz11']
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

# Initialize Plot #test
# https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
fig = go.Figure()
fig.add_trace(go.Scatter(name='Density', x=[0], y=[0], mode='lines',   marker_color=col_density, showlegend=True, hoverinfo='skip', line={'width': 3}, line_shape='spline', fill='tozerox'))
fig.add_trace(go.Scatter(name='Samples', x=[0], y=[0], mode='markers', marker_color=col_samples, marker_line_color='black', marker_opacity=1, showlegend=True))
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
        dcc.Slider(id="gauss2D-L", min=log10(1.2), max=4.001, step=0.001, value=2, updatemode='drag', marks=None,  # persistence=True,
                   tooltip={"template": "L={value}", "placement": "bottom", "always_visible": True, "transform": "trafo_L"}),

        # σ Slider
        dcc.Slider(id="gauss2D-σx", min=0, max=5, step=0.01, value=1, updatemode='drag', marks=None,
                   tooltip={"template": 'σx={value}', "placement": "bottom", "always_visible": True}),
        dcc.Slider(id="gauss2D-σy", min=0, max=5, step=0.01, value=1, updatemode='drag', marks=None,
                   tooltip={"template": 'σy={value}', "placement": "bottom", "always_visible": True}),

        # ρ Slider
        dcc.Slider(id="gauss2D-ρ", min=-1, max=1, step=0.001, value=0, updatemode='drag', marks=None,
                   tooltip={"template": 'ρ={value}', "placement": "bottom", "always_visible": True}),

        # angle Slider
        dcc.Slider(id="gauss2D-angle", min=0, max=360, step=1, value=0, updatemode='drag', marks=None,
                   tooltip={"template": 'angle={value}', "placement": "bottom", "always_visible": True}),

        # Description
        dcc.Markdown(
            r'''
            ## 2D Gaussian
            Interactive visualizaton of the bivariate Gaussian density

            $$
            f(\underline x) = \mathcal{N}(\underline x; \underline \mu, \textbf{C}) = 
            \frac{1}{2\pi \sqrt{\det(\textbf{C})}}
            \cdot \exp\!\left\{ -\frac{1}{2}
            \cdot (\underline x - \underline \mu)^\top \textbf{C}^{-1} (\underline x - \underline \mu) \right\} \enspace,
            \quad \underline{x}\in \mathbb{R}^2 \enspace, \quad \textbf{C} \enspace \text{positive semidefinite}  \enspace.
            $$

            ### Formulas and Literature
            - quantile function  
              $Q(p) = \sqrt{2}\, \mathrm{erf}^{-1}(2p-1)$
            - uniform to SND  
              $\underline x_i^{\text{SND}} = Q(\underline x_i^{\text{uni}})$
            - SND to Gauss: Cholesky  
              $\underline x_i^{\text{Gauss}} = \mathrm{chol}(\textbf{C}) \cdot \underline x_i^{\text{SND}}$
            - SND to Gauss: Eigendecomposition
              [[Frisch23](https://isif.org/media/generalized-eibonacci-grid-low-discrepancy-point-set-optimal-deterministic-gaussian), eq. 18], 
              [[Frisch21](https://ieeexplore.ieee.org/document/9626975), eq. 4]  
              $\underline x_i^{\text{Gauss}} = \mathbf{V} \cdot \sqrt{\mathbf{D}} \cdot \underline x_i^{\text{SND}}$
            - Fibonacci-Kronecker Lattice  
              $\underline x_i^{\text{uni}} = \begin{bmatrix}\mod( \Phi \cdot (i+z), 1) \\ \frac{2 i - 1 + \gamma}{2 L} \end{bmatrix} \enspace,
              \quad i \in \{1,2,\ldots,L\}\enspace, \quad z \in \mathbb{Z} \enspace, \quad \gamma\in[-1,1]$
            - LCD: Localized Cumulative Distribution 
              [[Hanebeck08](https://ieeexplore.ieee.org/document/4648104)],
              [[Hanebeck09](https://ieeexplore.ieee.org/document/5400649)],
              loaded from [library](https://github.com/KIT-ISAS/deterministic-samples-csv)  
              $K(\underline x - \underline m, b) = \exp\!\left\{ -\frac{1}{2} \cdot \left\Vert \frac{\underline x - \underline m}{b} \right\Vert_2^2 \right\} \enspace, \quad
              F(\underline m, b) = \int_{\mathbb{R}^2} f(\underline x) \, K(\underline x - \underline m, b) \, \mathrm{d} \underline x \enspace,$  
              $\widetilde f(x) = \mathcal{N}(\underline x; \underline 0, \textbf{I}) \enspace, \quad
              f(\underline x) = \sum_{i=1}^L \delta(\underline x - \underline x_i) \enspace,$  
              $D = \int_{\mathbb{R}_+} w(b) \int_{\mathbb{R}^2} \left( \widetilde F(\underline m, b) - F(\underline m, b) \right)^2 \mathrm{d} \underline m \, \mathrm{d} b \enspace,$  
              $\left\{\underline x_i^{\text{SND}}\right\}_{i=0}^L = \arg \min_{\underline x_i} \{D\}$
            - SP-Julier14: Sigma Points 
              [[Julier04](https://ieeexplore.ieee.org/document/1271397), eq. 12]  
              $L=2\cdot d + 1 \enspace, \quad i\in\{1,2,\dots,d\} \enspace,$  
              $\underline x_0=\underline 0 \enspace, \quad W_0 < 1 \enspace,$  
              $\underline x_i = \sqrt{\frac{L}{1-W_0}} \cdot \underline e_i \enspace, \quad W_i = \frac{1-W_0}{2 L} \enspace,$  
              $\underline x_{i+L} = -x_i \enspace, \quad W_{i+L} = W_i$
            - SP-Menegaz11: Minimum Sigma Set 
              [[Menegaz11](https://ieeexplore.ieee.org/abstract/document/6161480), eq. 2-8]  
              $L=d+1 \enspace, \quad i \in \{1,2, \dots d\} \enspace,$  
              $0 < w_0 < 1 \enspace, \quad 
              \alpha=\sqrt{\frac{1-w_0}{d}} \enspace, \quad
              C = \sqrt{\mathbf{I} - \alpha^2 \cdot \mathbf 1} \enspace, \quad
              \underline x_0 = - \frac{\alpha}{\sqrt{w_0}} \cdot \underline 1$  
              $w_{1\colon n} = \mathrm{diag}(w_0 \cdot \alpha^2 \cdot C^{-1} \cdot  \mathbf{1} \cdot (C^\top)^{-1}) \enspace,$  
              $\underline x_{1\colon n} = C \cdot (\sqrt{\mathbf{I} \cdot w_{1\colon n}})^{-1}$
            ### Interactivity
            - sampling methods (radiobutton)
                - Independent identically distributed (iid), the usual random samples. 
                - Fibonacci-Kronecker lattice, combination of 1D golden sequence and equidistant. Use with eigendecomposition for best homogeneity.
                - LCD SND samples. 
                - Sigma Points - Julier04.
            - transformation methods (radiobutton)
                - Cholesky decomposition. 
                - Eigenvalue-Eigenvector decomposition.
            - sampling parameter (slider)
                - iid: dice again
                - Fibonacci: integer offset 𝑧, offset 𝛾
                - LCD: SND rotation 𝛼, a proxy for dependency on initial guess during optimization
                - sigma points: scaling parameter
            - number of Samples 𝐿 (slider)
            - density parameters (slider)
                - standard deviation $\sigma_x$
                - standard deviation $\sigma_y$
                - correlation coefficient $\rho$
            ''',
            mathjax=True),
    ]), fluid=True, className="g-0")


@callback(
    Output('gauss2D-p', 'min'),
    Output('gauss2D-p', 'max'),
    Output('gauss2D-p', 'value'),
    Output('gauss2D-p', 'step'),
    Output('gauss2D-p', 'tooltip'),
    Output('gauss2D-L', 'disabled'),
    Input("gauss2D-smethod", "value"),
)
def update_smethod(smethod):
    patched_tooltip = Patch()
    match smethod:
        case 'iid':
            patched_tooltip.template = "dice"
            # min, max, value, step, tooltip
            return 0, 1, .5, 0.001, patched_tooltip, False
        case 'Fibonacci':
            patched_tooltip.template = "z={value}"
            return -50, 50, 0, 1, patched_tooltip, False
        case 'LCD':
            patched_tooltip.template = "α={value}°"
            return -360, 360, 0, 0.1, patched_tooltip, False
        case 'SP-Julier04':
            patched_tooltip.template = "W₀={value}"
            return -2, 1, .1, 0.001, patched_tooltip, True
        case 'SP-Menegaz11':
            patched_tooltip.template = "Wₙ₊₁={value}"
            return 0, 1, 1/3, 0.001, patched_tooltip, True
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
    Input("gauss2D-angle", "value"),
)
def update_sampling(smethod, tmethod, p, L0, σx, σy, ρ, angle):
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
    weights = None
    match smethod:
        case 'iid':
            xySND = randn(2, L)
        case 'Fibonacci':
            # TODO 2nd parameter
            xUni = (sqrt(5)-1)/2 * (arange(L)+1+round(p)) % 1
            yUni = (2*arange(L)+1)/(2*L)  # +p
            xyUni = vstack((xUni, yUni))
            xySND = sqrt(2)*erfinv(2*xyUni-1)
        case 'LCD':
            xySND = get_data(url_SND_LCD(2, L))
            xySND = matmul(rot(p), xySND)
        case 'SP-Julier04':
            # https://ieeexplore.ieee.org/abstract/document/1271397
            xySND,weights = update_julier(p, 2)
        case 'SP-Menegaz11':
            # https://ieeexplore.ieee.org/abstract/document/6161480
            xySND,weights = update_mengazz(p, 2)
        case _:
            raise Exception("Wrong smethod")
    match tmethod:
        case 'Cholesky':
            xyG = matmul(rot(angle),matmul(cholesky(C), xySND)) + μ
        case 'Eigendecomposition':
            xyG = matmul(rot(angle),matmul(C_R, sqrt(C_D) * xySND)) + μ
        case _:
            raise Exception("Wrong smethod")
    # Sample weights to scatter sizes
    L2 = xySND.shape[1]  # actual number of samples
    if L2 == 0:
        sizes = 10
    else:
        if weights is None:
            weights = 1/L2  # equally weighted
        else:
            weights = weights.flatten()
        sizes = sqrt(abs(weights) * L2) * det(2*pi*C)**(1/4) / sqrt(L2) * 70
    # print(hstack((cov(xyG, bias=True, aweights=weights), C)))

    # Plot Ellipse
    elp = matmul(rot(angle),matmul(C_R, sqrt(C_D) * circ)) + μ
    #print(elp)
    patched_fig['data'][0]['x'] = elp[0, :]
    patched_fig['data'][0]['y'] = elp[1, :]
    # Plot Samples
    patched_fig['data'][1]['x'] = xyG[0, :]
    patched_fig['data'][1]['y'] = xyG[1, :]
    patched_fig['data'][1]['marker']['size'] = sizes
    patched_fig['data'][1]['marker']['line']['width'] = sizes/20
    return patched_fig

@callback(
    Output("gauss2D-σx", "value"),
    Output("gauss2D-σy", "value"),
    Output("gauss2D-ρ", "value"),
    Output("gauss2D-angle", "value"),
    Input("gauss2D-L", "value"),
    Input("gauss2D-σx", "value"),
    Input("gauss2D-σy", "value"),
    Input("gauss2D-ρ", "value"),
    Input("gauss2D-angle", "value"),
)
def update_sliders(L0, σx, σy, ρ, angle):
    # Slider Transform,
    L = trafo_L(L0)
    # Mean
    # μ = array([[μx], [μy]])
    μ = array([[0], [0]])
    # Covariance
    C = array([[square(σx), σx*σy*ρ], [σx*σy*ρ, square(σy)]])
    slider_moved = ctx.triggered_id
    if(slider_moved == "gauss2D-angle"): # if the angle was changed 
        oldCvariance = eigen_rec(C,angle)
        C = oldCvariance
        #print(oldCvariance)
        print(angle)
        σx, σy, ρ = calculate_new_cov_values(oldCvariance)
    if(slider_moved == "gauss2D-σx" or slider_moved == "gauss2D-σy" or slider_moved == "gauss2D-ρ"):
        angle = eigen_dec(C) # if σ, or ρ was changed
    return σx, σy, ρ, angle 

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

def eigen_dec(c): #decompose covariance matrix
    eigenValues, eigenVectors = eig(c) #calculate eigendecomposition
    maxColumn = list(eigenValues).index(max(eigenValues))
    onlyEigenVectors = eigenVectors[:,maxColumn]
    #print(onlyEigenVectors)
    newangleRadian = atan2(onlyEigenVectors[1],onlyEigenVectors[0])
    newangle = math.degrees(newangleRadian)
    return newangle

def eigen_rec(c, angle): #reconstruct covariance matrix
    newCovariance =  matmul(rot(angle), matmul(c, rot(angle).T))  # matmul(rot(angle), matmul(rotCovariance, rot(angle).T))
    #print(newCovariance)
    return newCovariance

def calculate_new_cov_values(c): #calculate new values
    σx = round(sqrt(c[0,0]),4)
    σy = round(sqrt(c[1,1]),4)
    ρ = round(c[0,1]/(σx * σy),4)
    #print(σx, σy, ρ)
    return σx, σy, ρ