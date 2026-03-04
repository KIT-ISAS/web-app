from abc import ABC, abstractmethod
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.silder_log import LogSlider 
import numpy as np
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI

class TorusRandomWrappedSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000))
		]

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		mean_x = distribution_options[0].state
		mean_y = distribution_options[1].state
		sigma_t = distribution_options[2].state
		sigma_p = distribution_options[3].state
		correlation = distribution_options[4].state

		Cov = np.array([
			[sigma_t**2, correlation * sigma_t * sigma_p],
			[correlation * sigma_t * sigma_p, sigma_p**2]
		])

		mean = np.array([mean_x, mean_y])

		samples = np.random.multivariate_normal(mean, Cov, sample_count)
		samples[:,0] = samples[:,0] % (2 * np.pi)
		samples[:,1] = samples[:,1] % (2 * np.pi)
		
		
		return samples