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
	[[Frisch23](https://isif.org/media/generalized-fibonacci-grid-low-discrepancy-point-set-optimal-deterministic-gaussian), eq. 18], 
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
- GUI
	- add/remove lines: click in legend
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