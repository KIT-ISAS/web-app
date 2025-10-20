from abc import ABC, abstractmethod
import numpy as np
import scipy

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider import Slider 


class VonMisesRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 1, 50, 500),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state
		kappa = distribution_options[0].state

		samples = scipy.stats.vonmises_fisher.rvs(mu=[0,0,1], kappa=kappa, size=sample_count)

		return samples