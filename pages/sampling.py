import plotly
import dash
import pandas
from urllib.error import HTTPError
from dash import dcc, html, Input, Output, callback, Patch
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, vstack, hstack, pi, nan, full, exp, square, arange, array, sin, cos, diff, matmul, log10, deg2rad, identity, ones, zeros, diag, cov, mean
from numpy.random import randn, randint
from numpy.linalg import cholesky, eig, det, inv
from scipy.special import erfinv


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
            Nx = int   # dimension
            x0 = zeros([Nx, 1])
            W0 = full([1, 1], p)  # parameter, W0<1
            x1 = sqrt(Nx/(1-W0) * identity(Nx))
            W1 = full([1, Nx], (1-W0)/(2*Nx))
            if Nx > 1:
                x2 = -x1
                W2 = W1
                xySND = hstack((x0, x1, x2))
                weights = hstack((W0, W1, W2))
            else:
                xySND = hstack((x0,x1))
                weights = hstack((W0,W1))
        case 'SP-Menegaz11':
            # https://ieeexplore.ieee.org/abstract/document/6161480
            n = int  # dimension
            w0 = p  # parameter, 0<w0<1
            α = sqrt((1-w0)/n)
            CC2 = identity(n) - α**2
            CC = cholesky(CC2)
            w1 = diag(w0 * α**2 * matmul(matmul(inv(CC), ones([n, n])), inv(CC.T)))
            x0 = full([n, 1], -α/sqrt(w0))
            x1 = matmul(CC, inv(identity(n)*sqrt(w1)))
            # x1 = CC / sqrt(W1)
            xySND = hstack((x0, x1))
            weights = hstack((p, w1))
        case _:
            raise Exception("Wrong smethod")
    match tmethod:
        case 'Cholesky':
            xyG = matmul(cholesky(C), xySND) + μ
        case 'Eigendecomposition':
            xyG = matmul(C_R, sqrt(C_D) * xySND) + μ
        case _:
            raise Exception("Wrong smethod")
    # Sample weights to scatter sizes
    L2 = xySND.shape[1]  # actual number of saamples
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
    elp = matmul(C_R, sqrt(C_D) * circ) + μ
    patched_fig['data'][0]['x'] = elp[0, :]
    patched_fig['data'][0]['y'] = elp[1, :]
    # Plot Samples
    patched_fig['data'][1]['x'] = xyG[0, :]
    patched_fig['data'][1]['y'] = xyG[1, :]
    patched_fig['data'][1]['marker']['size'] = sizes
    patched_fig['data'][1]['marker']['line']['width'] = sizes/20
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
