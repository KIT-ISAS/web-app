import numpy as np
from scipy.stats import norm
from deterministic_gaussian_sampling_fibonacci import get_uniform_grid


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
	
	@staticmethod
	def sample_frolov_gaussian(mu, cov, sample_count, variant="ClassicalFrolov"):
		grid = get_uniform_grid(2, sample_count, variant)
		gaus_grid = GausUtil.transform_grid_gaussian(grid, mu, cov)
		return gaus_grid