import numpy as np

from util.selectors.silder_log import LogSlider
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI
from util.gaus_util import GausUtil as gu


class TorusFibKroneckerWNSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000))
		]

	def get_name(self):
		return "Fibonacci-Kronecker Lattice"
	
	def sample(self, sample_options, distribution_options):
		# see https://isas.iar.kit.edu/pdf/Fusion21_Frisch.pdf
		sample_count = sample_options[0].state

		indices = np.arange(0, sample_count)
		gol = (1+5**0.5)/2
		
		# centered rank-1 lattice generator
		equidistant_generator = (2 * indices + 1) / (2 * sample_count)
		
		t = equidistant_generator
		p = (indices / gol) % 1


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