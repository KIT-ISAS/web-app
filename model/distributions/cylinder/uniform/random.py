from abc import ABC, abstractmethod
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.silder_log import LogSlider 
import numpy as np

class CylinderRandomUniformSampling(CylinderSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000)
		]

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		t = np.random.uniform(0, 2 * np.pi, sample_count)
		p = np.random.uniform(0, 2 * np.pi, sample_count)

		samples = np.column_stack((t, p))

		return samples