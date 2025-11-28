import numpy as np
from scipy.stats import norm

class GausUtil:
	@staticmethod
	def transform_grid_gaussian(grid, mu, cov):
		eps = 1e-9
		grid = np.clip(grid, eps, 1 - eps) # avoid inf in ppf

		gaus = norm.ppf(grid)

		var = np.mean(gaus**2, axis=0)

		gaus = gaus / np.sqrt(var)

		# scale with eigen decomposition
		ew, V = np.linalg.eig(cov)

		D = np.diag(np.sqrt(ew))	

		gaus = gaus.T	# (2,L)

		gaus = V @ D @ gaus # (2,2) @ (2,2) @ (2,L) -> (2,L)

		gaus = gaus.T # (L,2)

		gaus[:,0] += mu[0]
		gaus[:,1] += mu[1]

		return gaus