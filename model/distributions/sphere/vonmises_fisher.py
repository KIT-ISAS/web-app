from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
import numpy as np
import scipy

class SphereDistribution(SphereDistribution):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 1, 50, 1000),
			Slider("Kappa (κ)", 1, 5, 15),
		]
		
		self.distribution_options = []

	def get_name(self):
		return "von Mises-Fisher"
	
	def sample(self, sample_options):
		sample_count = sample_options[0].state
		kappa = sample_options[1].state

		samples = scipy.stats.vonmises_fisher.rvs(mu=[0,0,1], kappa=kappa, size=sample_count)

		return samples

	def generate_mesh(self, distribution_options):
		pass