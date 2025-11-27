from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm

from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_fib import SliderFib
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class TorusFibRank1WNSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderFib("Number of Samples", 2, 34, 21, 9))
		]
		self.sampler = CylinderFibRank1UniformSampling()

	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"
	
	def sample(self, sample_options, distribution_options):
		# see https://isas.iar.kit.edu/pdf/Fusion21_Frisch.pdf
		sample_count = sample_options[0].state

		t, p = self.sampler.get_rank_1(sample_count, sample_options[0].idx)

		fib_grid = np.column_stack((t , p))

		mean_x = distribution_options[0].state
		mean_y = distribution_options[1].state
		sigma_t = distribution_options[2].state
		sigma_p = distribution_options[3].state
		correlation = distribution_options[4].state

		Cov = np.array([
			[sigma_t**2, correlation * sigma_t * sigma_p],
			[correlation * sigma_t * sigma_p, sigma_p**2]
		])
		
		gaus_grid = self.transform_grid_gaussian(fib_grid, (mean_x, mean_y), Cov)

		# wrapp
		gaus_grid[:,0] = gaus_grid[:,0] % (2 * np.pi)
		gaus_grid[:,1] = gaus_grid[:,1] % (2 * np.pi)
		return gaus_grid


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