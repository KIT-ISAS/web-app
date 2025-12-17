from pathlib import Path
import plotly
import dash
import pandas
from urllib.error import HTTPError
from dash import dcc, html, Input, Output, callback, Patch, ctx, no_update
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
from numpy import sqrt, linspace, vstack, hstack, pi, nan, full, exp, square, arange, array, sin, cos, diff, matmul, log10, deg2rad, identity, ones, zeros, diag, cov, mean
from numpy.random import randn, randint
from numpy.linalg import cholesky, eig, det, inv
from scipy.special import erfinv


from components.popup_box import PopupBox
from model.selfcontained_distribution import SelfContainedDistribution

# Samples Library
# technically, this has state, but its fine because its just a cache
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

class Gaus2D(SelfContainedDistribution):
	def __init__(self):
		self.smethods = ['iid', 'Fibonacci', 'LCD', 'SP-Julier04', 'SP-Menegaz11'] # Sampling methods
		self.tmethods = ['Cholesky', 'Eigendecomposition'] # Transformation methods

		# Colors
		self.col_density = plotly.colors.qualitative.Plotly[1]
		self.col_samples = plotly.colors.qualitative.Plotly[0]

		self.config = {
			'toImageButtonOptions': {
				'format': 'jpeg',  # png, svg, pdf, jpeg, webp
				'height': None,   # None: use currently-rendered size
				'width': None,
				'filename': 'gauss2d',
			},
			'scrollZoom': True,
		}

		# axis limits
		self.rangx = [-5, 5]
		self.rangy = [-4, 4]

		# plot size relative to window size
		relwidth = 95
		self.relheight = round((relwidth/diff(self.rangx)*diff(self.rangy))[0])

		# Gauss ellipse
		s = linspace(0, 2*pi, 500)
		self.circ = vstack((cos(s), sin(s))) * 2

		self.fig = go.Figure(
			data=[
				go.Scattergl(name='Density',
					x=[0], 
					y=[0], 
					mode='lines',   
					marker_color=self.col_density, 
					showlegend=True, 
					hoverinfo='skip', 
					line={'width': 3}, 
					line_shape='linear', 
					fill='toself'
				),
				go.Scattergl(
					name='Samples', 
					x=[0], 
					y=[0], 
					mode='markers', 
					marker_color=self.col_samples, 
					marker_line_color='black', 
					marker_opacity=1, 
					showlegend=True
				)
			],
		)
		self.fig.update_xaxes(range=self.rangx, tickmode='array', tickvals=list(range(self.rangx[0], self.rangx[1]+1)))
		self.fig.update_yaxes(range=self.rangy, tickmode='array', tickvals=list(range(self.rangy[0], self.rangy[1]+1)), scaleanchor="x", scaleratio=1)
		self.fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
		self.fig.update_layout(modebar_add=['drawopenpath', 'eraseshape'], newshape_line_color='cyan', dragmode='pan')

		self.fig.update_layout(
			legend=dict(
				orientation="v",
				xanchor="right",
				x=0.1,
			)
		)

		path = Path(__file__).parent / "info_text.md"
		with open(path, 'r') as f:
			self.info_text = dcc.Markdown(f.read(), mathjax=True)

		self.settings_layout = [
			dbc.Container(
				dbc.Col([
					html.P("Select Sampling Method:"),
					html.Br(),

					# Sampling Strategy RadioItems
					dbc.RadioItems(id='gauss2D-smethod',
								options=[{"label": x, "value": x} for x in self.smethods],
								value=self.smethods[randint(len(self.smethods))],
								inline=True),

					# Transformation Method RadioItems
					dbc.RadioItems(id='gauss2D-tmethod',
								options=[{"label": x, "value": x} for x in self.tmethods],
								value=self.tmethods[randint(len(self.tmethods))],
								inline=True),

					html.Br(),
					html.Hr(),
					html.Br(),

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
					
					# ρ Slider
					dcc.Slider(id="angle", min=0, max=180, step=2, value=0, updatemode='drag', marks=None,
							tooltip={"template": 'angle={value}°', "placement": "bottom", "always_visible": True}),

					html.Hr(),
					html.Br(),


					# Info Popup
					*PopupBox("gauss2D-info", "Learn More", "Additional Information", self.info_text),
				]), 
				fluid=True,
				className="g-0")
		]

		self.plot_layout = [
			dcc.Graph(id="gauss2D-graph", figure=self.fig, config=self.config, style={'height': '100%'}),
		]

		self._register_callbacks()

	def _register_callbacks(self):
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
			Output("gauss2D-σx", "value"),
			Output("gauss2D-σy", "value"),
			Output("gauss2D-ρ", "value"),
			Output("angle", "value"),
			Input("gauss2D-smethod", "value"),
			Input("gauss2D-tmethod", "value"),
			Input("gauss2D-p", "value"),
			Input("gauss2D-L", "value"),
			Input("gauss2D-σx", "value"),
			Input("gauss2D-σy", "value"),
			Input("gauss2D-ρ", "value"),
			Input("angle", "value"),
		)
		def update(smethod, tmethod, p, L0, sigma_x, sigma_y, rho, angle):
			trig = ctx.triggered_id

			def _rot2d(angle_deg):
				a = np.deg2rad(angle_deg)
				c, s = np.cos(a), np.sin(a)
				return np.array([[c, -s],
								[s,  c]], dtype=float)
			
			
			

			if trig == "angle":
				R = _rot2d(angle)
				C = np.array([[sigma_x**2, sigma_x*sigma_y*rho],
							  [sigma_x*sigma_y*rho, sigma_y**2]])
				w, _ = np.linalg.eigh(C)
				w = np.sort(w)[::-1]
				C_rot = R @ np.diag(w) @ R.T
				sigma_x = np.sqrt(C_rot[0, 0])
				sigma_y = np.sqrt(C_rot[1, 1])
				if sigma_x > 0:
					rho = C_rot[0, 1] / (sigma_x * sigma_y)
				else:
					rho = 0.0
				silder_changes = (sigma_x, sigma_y, rho, no_update)
			else:
				if np.isclose(rho, 0) and np.isclose(sigma_x, sigma_y):
					angle = 0.0
				else:
					angle = 0.5 * np.arctan2(2 * rho * sigma_x * sigma_y, sigma_x**2 - sigma_y**2)
					angle = np.rad2deg(angle)
					angle = angle % 180
				silder_changes = (no_update, no_update, no_update, angle)
				

			# Slider Transform,
			L = self.trafo_L(L0)
			# Mean
			# μ = array([[μx], [μy]])
			μ = array([[0], [0]])
			# Covariance
			C = array([[square(sigma_x), sigma_x*sigma_y*rho], [sigma_x*sigma_y*rho, square(sigma_y)]])
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
					xySND = get_data(self.url_SND_LCD(2, L))
					xySND = matmul(self.rot(p), xySND)
				case 'SP-Julier04':
					# https://ieeexplore.ieee.org/abstract/document/1271397
					Nx = 2   # dimension
					x0 = zeros([Nx, 1])
					W0 = full([1, 1], p)  # parameter, W0<1
					x1 = sqrt(Nx/(1-W0) * identity(Nx))
					W1 = full([1, Nx], (1-W0)/(2*Nx))
					x2 = -x1
					W2 = W1
					xySND = hstack((x0, x1, x2))
					weights = hstack((W0, W1, W2))
				case 'SP-Menegaz11':
					# https://ieeexplore.ieee.org/abstract/document/6161480
					n = 2  # dimension
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
			# Plot Ellipse
			elp = matmul(C_R, sqrt(C_D) * self.circ) + μ
			patched_fig['data'][0]['x'] = elp[0, :]
			patched_fig['data'][0]['y'] = elp[1, :]
			# Plot Samples
			patched_fig['data'][1]['x'] = xyG[0, :]
			patched_fig['data'][1]['y'] = xyG[1, :]
			patched_fig['data'][1]['marker']['size'] = sizes
			patched_fig['data'][1]['marker']['line']['width'] = sizes/20
			return patched_fig, *silder_changes

	
	@staticmethod
	def url_SND_LCD(D, L):
		return f'https://raw.githubusercontent.com/KIT-ISAS/deterministic-samples-csv/main/standard-normal/glcd/D{D}-N{L}.csv'
	
	@staticmethod
	def gauss1(x, μ, σ):
		return 1/sqrt(2*pi*σ) * exp(-1/2 * square((x-μ)/σ))
	
	
	# Slider Transform, must be idencital to window.dccFunctions.trafo_L in assets/tooltip.js
	@staticmethod
	def trafo_L(L0):
		if L0 < log10(1.25):
			return 0
		else:
			return round(10 ** L0)
		
	@staticmethod
	def rot(a):
		ar = deg2rad(a)
		return array([[cos(ar), -sin(ar)], [sin(ar), cos(ar)]])
	
		


