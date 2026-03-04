from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm

from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_fib import SliderFib
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI
from util.gaus_util import GausUtil as gu

class TorusFibRank1WNSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderFib("Number of Samples", 3, 33, 21, 9, minus_1=True))
		]
		self.sampler = CylinderFibRank1UniformSampling()

	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"
	
	def sample(self, sample_options, distribution_options):
		# see https://isas.iar.kit.edu/pdf/Fusion21_Frisch.pdf
		sample_count = sample_options[0].state + 1 # because minus_1 is true slider displays fib(n)-1

		t, p = self.sampler.get_rank_1(sample_count, sample_options[0].idx, without_first_point=True)

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
		
		gaus_grid = gu.transform_grid_gaussian(fib_grid, (mean_x, mean_y), Cov)

		# wrapp
		gaus_grid[:,0] = gaus_grid[:,0] % (2 * np.pi)
		gaus_grid[:,1] = gaus_grid[:,1] % (2 * np.pi)
		return gaus_grid


	