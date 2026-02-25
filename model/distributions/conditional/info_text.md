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