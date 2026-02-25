import numpy as np

class CartesianUtil:
	
	""" Generate a Cartesian grid of samples.
		n: number of samples along one dimension (total samples = n*n)
		widths: tuple of widths along each dimension
		Returns: array of shape (n*n, 2) with samples
	"""
	@staticmethod
	def generate_cartesian_grid(n, widths):
		indices = np.arange(n)

		# use cell centers of an n x n grid on [0, 1) x [0, 1), then scale to widths
		t = (indices + 0.5) / n * widths[0]
		p = (indices + 0.5) / n * widths[1]

		t_grid, p_grid = np.meshgrid(t, p, indexing="ij")

		return np.column_stack((t_grid.ravel(), p_grid.ravel()))