import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, vstack, hstack, pi, nan, full, exp, square, arange, array, sin, cos, diff, matmul, log10, deg2rad, identity, ones, zeros, diag, cov, mean
from numpy.random import randn, randint
from numpy.linalg import cholesky, eig, det, inv
from scipy.special import erfinv

def update_julier(smethod, tmethod, p, L0, σx, σy, ρ, Nx): #Nx = dimension
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


    
def update_mengazz(smethod, tmethod, p, L0, σx, σy, ρ, dim): #dim = dimension
    # https://ieeexplore.ieee.org/abstract/document/6161480
    n = dim  # dimension
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