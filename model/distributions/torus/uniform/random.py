from abc import ABC, abstractmethod
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.slider import Slider 
import numpy as np

class TorusRandomUniformSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 10, 100, 1000)
		]

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		t = np.random.uniform(0, 2 * np.pi, sample_count)
		p = np.random.uniform(0, 2 * np.pi, sample_count)

		samples = np.column_stack((t, p))

		return samples