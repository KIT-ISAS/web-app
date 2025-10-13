from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
import numpy as np

class SphereDistribution(SphereDistribution):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 10, 100, 1000)
		]
		
		self.distribution_options = []

	def get_name(self):
		return "Random"
	
	def sample(self, sample_options):
		sample_count = sample_options[0].state

		samples = np.random.normal(size=(sample_count, 3))
		samples /= np.linalg.norm(samples, axis=1)[:, np.newaxis]

		return samples

	def generate_mesh(self, distribution_options):
		pass