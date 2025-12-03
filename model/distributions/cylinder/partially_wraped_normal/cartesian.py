from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm

from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_square import SliderSquare
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI
from util.gaus_util import GausUtil as gu
from util.cartesian_util import CartesianUtil as cu

class CylinderFibCartPWNSampling(CylinderSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderSquare("Number of Samples", 4, 16, 100, 4))
		]
		self.sampler = CylinderFibRank1UniformSampling()
		self.info_md = """
		> Warning: Using the Cartesian Grid is not recomended in practise, as it yields bad results.
		> Sample count may appear off due to samples overlapping.
		> It is included for demonstration purposes only."""

	def get_name(self):
		return "Cartesian Grid"
	
	def sample(self, sample_options, distribution_options):
		# see https://isas.iar.kit.edu/pdf/Fusion21_Frisch.pdf
		sample_count = sample_options[0].state

		n = int(np.sqrt(sample_count))

		grid = cu.generate_cartesian_grid(n, (1.0, 1.0))

		mean_x = distribution_options[0].state
		mean_y = distribution_options[1].state
		sigma_t = distribution_options[2].state
		sigma_p = distribution_options[3].state
		correlation = distribution_options[4].state

		Cov = np.array([
			[sigma_t**2, correlation * sigma_t * sigma_p],
			[correlation * sigma_t * sigma_p, sigma_p**2]
		])
		
		gaus_grid = gu.transform_grid_gaussian(grid, (mean_x, mean_y), Cov)

		# wrap
		gaus_grid[:,0] = gaus_grid[:,0] % (2 * np.pi)
		return gaus_grid


	
