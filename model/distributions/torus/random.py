from abc import ABC, abstractmethod
from model.distributions.torus.torus_distribution import TorusDistribution
from util.selectors.slider import Slider 
import numpy as np

class SphereDistribution(TorusDistribution):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 10, 100, 1000)
		]
		self.distribution_options = []

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options):
		sample_count = sample_options[0].state

		t = np.random.uniform(0, 2 * np.pi, sample_count)
		p = np.random.uniform(0, 2 * np.pi, sample_count)

		samples = np.column_stack((t, p))

		return samples

	def generate_mesh(self, distribution_options):
		pass