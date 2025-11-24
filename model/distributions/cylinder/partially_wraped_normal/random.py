from abc import ABC, abstractmethod
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.silder_log import LogSlider 
import numpy as np

class CylinderRandomPWNSampling(CylinderSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000)
		]

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		sigma_x = distribution_options[0].state
		sigma_y = distribution_options[1].state
		correlation = distribution_options[2].state

		Cov = np.array([
			[sigma_x**2, correlation * sigma_x * sigma_y],
			[correlation * sigma_x * sigma_y, sigma_y**2]
		])

		mean = np.array([np.pi, np.pi])

		samples = np.random.multivariate_normal(mean, Cov, sample_count)
		samples[:,0] = samples[:,0] % (2 * np.pi)
		
		
		return samples