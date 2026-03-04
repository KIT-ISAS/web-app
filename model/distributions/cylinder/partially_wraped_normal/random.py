from abc import ABC, abstractmethod
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.silder_log import LogSlider 
import numpy as np
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class CylinderRandomPWNSampling(CylinderSamplingSchema):
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
		sigma_x = distribution_options[2].state
		sigma_y = distribution_options[3].state
		correlation = distribution_options[4].state

		Cov = np.array([
			[sigma_x**2, correlation * sigma_x * sigma_y],
			[correlation * sigma_x * sigma_y, sigma_y**2]
		])

		mean = np.array([mean_x, mean_y])

		samples = np.random.multivariate_normal(mean, Cov, sample_count)
		samples[:,0] = samples[:,0] % (2 * np.pi)
		
		
		return samples