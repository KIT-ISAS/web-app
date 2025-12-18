import numpy as np
from deterministic_gaussian_sampling_fibonacci import sample_gaussian_fibonacci

from util.selectors.silder_log import LogSlider
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI
from util.gaus_util import GausUtil as gu


class CFrolovWNSampling(TorusSamplingSchema):
	def __init__(self):
		def _check_input(val):
			return val >= 1 and val <= 100003 and isinstance(val, int)

		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000))
		]

	def get_name(self):
		return "Classical Frolov"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		mean_x = distribution_options[0].state
		mean_y = distribution_options[1].state
		sigma_t = distribution_options[2].state
		sigma_p = distribution_options[3].state
		correlation = distribution_options[4].state

		mu = np.array([mean_x, mean_y])

		Cov = np.array([
			[sigma_t**2, correlation * sigma_t * sigma_p],
			[correlation * sigma_t * sigma_p, sigma_p**2]
		])
		
		gaus_grid = sample_gaussian_fibonacci(mu, Cov, sample_count, "ClassicalFrolov")

		# wrapp
		gaus_grid[:,0] = gaus_grid[:,0] % (2 * np.pi)
		gaus_grid[:,1] = gaus_grid[:,1] % (2 * np.pi)
		return gaus_grid