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

        TODO:
        - Sample Reduction
        - 1D Gauss: add sigma points and weights; use Patch update; dice with button; add LCD; add Sobol
        - 2D Gauss: add rotation angle; dice with button; add 2nd paramter for Fibonacci; Fibonacci-rk1; 
          Fibonacci-Kron; add Sobol; adjust sample size according to figure size
        - 2D Gauss Density (no samples but show covariance marginals, det, trace, and marginals)
        - 3D Gauss: Mesh3d, scatter_3d, trisurf, Isosurface
        - strong / weak nonlinearity 
        - 2D Filter Step
        - 3D Filter Step: go.Volume
        - Nginx HTTP server: port 80 -> 8080 
        - gunicorn multi-processing deployment
        - Browser tab: symbol & name 
        - Domain, Certificate HTTPS
        - Sankey / Parallel Categories: filtering variants
        - Treemap: numbers, filters, 
        - Quiver / Streamline: progressive filters / system model
        - Tracking example: 3D Line
        - trisurf, Isosurface: sample on sphere, torus, 
        - make plots resizable: https://stackoverflow.com/questions/17855401/how-do-i-make-a-div-width-draggable 
        - Distributed Sampling: Fusion of two 2D Gaussians; show naive, CI, ICI; sliders for 4 variances, 2 visible and 4 hidden correlations
        '''
        )
], fluid=True, className="g-0")
