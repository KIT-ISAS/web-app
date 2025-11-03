from abc import ABC, abstractmethod
import numpy as np

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider 

class SphereUniformRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000)
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		samples = np.random.normal(size=(sample_count, 3))
		samples /= np.linalg.norm(samples, axis=1)[:, np.newaxis]

		return samples