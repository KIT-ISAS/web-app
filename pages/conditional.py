import plotly
import dash
from dash import dcc, html, Input, Output, callback, Patch, callback_context
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sqrt, linspace, pi, sign, exp, square, array, diff, matmul, zeros, meshgrid
from numpy.random import randint
from numpy.linalg import det, solve

from components.popup_box import PopupBox
from components.split_pane import SplitPane
from components.label import Label

dash.register_page(__name__)

# Colors
col_marginal = plotly.colors.qualitative.Plotly[0]
col_conditional = plotly.colors.qualitative.Plotly[1]
col_slice = plotly.colors.qualitative.Plotly[4]
# axis limits
rangx = [-4, 4]
rangy = [-4, 4]
# slider range
smin = rangy[0]
smax = rangy[1]
# plot size relative to window size
relwidth = 95
relheight = round((relwidth/diff(rangx)*diff(rangy))[0])

# Grid
xv = linspace(rangx[0], rangx[1], 100)
yv = linspace(rangy[0], rangy[1], 100)
xm, ym = meshgrid(xv, yv)


def gauss1(x, μ, C):
	return 1/sqrt(2*pi*C) * exp(-1/2 * square((x-μ))/C)


def gauss2(x, y, μ, C):
	d = array([x-μ[0], y-μ[1]])
	d = d.reshape(-1, 1)  # to column vector
	f = 1/sqrt(det(2*pi*C)) * exp(-1/2 * matmul(d.T, solve(C, d)))
	return f[0][0]


# Initialize Plot
# https://plotly.com/python/3d-surface-plots/
fig = go.Figure()
fig.add_trace(go.Surface(name='Joint f(x,y)', x=xm, y=ym, z=xm*0, hoverinfo='skip', colorscale='Cividis', showlegend=True, showscale=False, reversescale=False, contours={"z": {"show": True, "start": 0.1, "end": 1, "size": 0.1, "width": 1, "color": "white"}}))
# fig.add_trace(go.Mesh3d(name='Joint', x=x, y=y, z=z, intensity=z, colorscale='Viridis')) # can deal with vector xyz, but hover coords not in foreground
fig.add_trace(go.Scatter3d(name='Marginal f(x)', x=xv, y=yv*0+yv[0], mode='lines', z=xv*0, marker_color=col_marginal, showlegend=True, hoverinfo='skip', line={'width': 10}))  # , surfaceaxis=2 wait for: https://github.com/plotly/plotly.js/issues/2352
fig.add_trace(go.Scatter3d(name='Conditional f(x|ŷ)', x=xv, y=yv*0+yv[0], mode='lines', z=xv*0, marker_color=col_conditional, showlegend=True, hoverinfo='skip', line={'width': 4}))  # , surfaceaxis=2 wait for: https://github.com/plotly/plotly.js/issues/2352
fig.add_trace(go.Scatter3d(name='Slice f(x,ŷ)', x=xv, y=yv*0+yv[0], mode='lines', z=xv*0, marker_color=col_slice, showlegend=True, hoverinfo='skip', line={'width': 8}))  
fig.update_xaxes(range=rangx, tickmode='array', tickvals=list(range(rangx[0], rangx[1]+1)))
fig.update_yaxes(range=rangy, tickmode='array', tickvals=list(range(rangy[0], rangy[1]+1)), scaleanchor="x", scaleratio=1)
fig.update_layout(transition_duration=100, transition_easing='linear')
fig.update_scenes(camera_projection_type="orthographic")
fig.update_scenes(aspectmode="cube")
# fig.update_scenes(xaxis_nticks=1)
# fig.update_scenes(yaxis_nticks=1)
fig.update_scenes(zaxis_nticks=1)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

fig.update_layout(
	legend=dict(
		orientation="v",
		yanchor="top",
		y=0.99,
		xanchor="right",
		x=0.1,
	)
)

config = {
	'toImageButtonOptions': {
		'format': 'png',  # png, svg, pdf, jpeg, webp
		'width':  None,   # None: use currently-rendered size
		'height': None,
		'filename': 'conditional',
	},
	'responsive': True,
	'scrollZoom': True,
}


# Description
info_text = dcc.Markdown(
	r'''
	## 2D Gaussian
	Interactive visualizaton of the 2D Gaussian and its marginal and conditional density. 

	$$
	f(\underline x) = \mathcal{N}(\underline x; \underline \mu, \textbf{C}) = 
	\frac{1}{2\pi \sqrt{\det(\textbf{C})}}
	\cdot \exp\!\left\{ -\frac{1}{2}
	\cdot (\underline x - \underline \mu)^\top \textbf{C}^{-1} (\underline x - \underline \mu) \right\} \enspace,
	\quad \underline{x}\in \mathbb{R}^2 \enspace, \quad \textbf{C} \enspace \text{positive semidefinite}  \enspace.
	$$

	### Formulas and Literature
	The Gaussian parameters are restricted to 
	$$
	\underline \mu = \begin{bmatrix}0 \\ 0\end{bmatrix}\,, \quad 
	\textbf{C} = \begin{bmatrix}1 & \rho \\ \rho & 1\end{bmatrix} \enspace. 
	$$

	Formulas for marginalization and conditioning of are given in the 
	[[MatrixCookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)]. 
	
	Note that the 1D and 2D densities are scaled with respect to each other such that 2D joint and 1D marginal have 
	the same height and therefore the same shape when looking on the x-z plane. 


	### Interactivity
	- GUI
		- rotate: left mouse click
		- pan: right mouse click
		- zoom: mouse wheel
		- add/remove lines: click in legend
	- value in state space (slider)
		- value to condition on $\hat{y}$ 
	- density parameter (slider)
		- correlation coefficient $\rho$
	''',
	mathjax=True
)

layout = SplitPane([
	dbc.Container(
		dbc.Col([
			html.Br(),

			# y Slider
			Label("Condition on ŷ", 
				dcc.Slider(
					id="joint-y",
					min=smin,
					max=smax, 
					value=randint(smin*10, smax*10)/10, 
					updatemode='drag', marks=None,
					tooltip={"template": "ŷ={value}", "placement": "bottom", "always_visible": True}
				),
			),

			# ρ Slider
			Label("Correlation ρ",
				dcc.Slider(
					id="joint-ρ", 
					min=-1, max=1, 
					value=randint(-9, 9)/10, 
					updatemode='mouseup', 
					marks=None,
					tooltip={"template": "ρ={value}", "placement": "bottom", "always_visible": True}
				)
			),

			html.Hr(),
			html.Br(),

			# Info Popup
			*PopupBox("joint-info", "Learn More", "Additional Information", info_text),
			
		]), 
		fluid=True,
		className="g-0"),
	],
	[
		# Plot
		dcc.Graph(id="joint-graph", figure=fig, config=config, style={'height': '100%'}), 
	],
	30
)

@callback(
	Output("joint-graph", "figure"),
	Input("joint-y", "value"),
	Input("joint-ρ", "value"),
)
def update(ys, ρ):
	patched_fig = Patch()
	# Joint Parameters
	μ = zeros([2, 1])
	sx = 1
	sy = 1
	# TODO special treatment for singular density
	ρ = sign(ρ) * min(abs(ρ), .9999)
	C = array([[sx**2, sx*sy*ρ], [sx*sy*ρ, sy**2]])
	# Marginal Parameters
	µMarginal = µ[0]
	CMarginal = C[0, 0]
	marginal_fac = 1 / gauss1(0, 0, CMarginal)
	# Density has been modified? 
	if (callback_context.triggered_id == "joint-ρ") | (callback_context.triggered_id is None):
		zMarginal = gauss1(xv, µMarginal, CMarginal) 
		patched_fig['data'][1]['z'] = zMarginal * marginal_fac
		# Compute new joint density values
		# TODO should be more elegant than 2 for loops
		zJoint = xm*0
		for i in range(xm.shape[0]):
			for j in range(xm.shape[1]):
				zJoint[i, j] = gauss2(xm[i, j], ym[i, j], μ, C)
		zJoint = zJoint / gauss2(0, 0, zeros([2, 1]), C)  # rescale to height 1
		patched_fig['data'][0]['z'] = zJoint
	# Compute Conditional
	# https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf
	µCond = µ[0] + C[0, 1] / C[1, 1] * (ys-µ[1])
	CCond = C[0, 0] - C[0, 1] / C[1, 1] * C[0, 1]
	zCond = gauss1(xv, µCond, CCond) 
	zSlice = zCond / gauss1(0, 0, CCond) * gauss1(ys, µ[1], C[1, 1]) / gauss1(0, 0, C[1, 1]) 
	# Plot Conditional
	patched_fig['data'][2]['z'] = zCond * marginal_fac
	# Plot Joint Slice
	patched_fig['data'][3]['y'] = xv*0+ys
	patched_fig['data'][3]['z'] = zSlice + 1e-3
	return patched_fig
