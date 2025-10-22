from abc import ABC, abstractmethod
import numpy as np
import scipy
import sphstat

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider import Slider 


class BinghamRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 1, 50, 100),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		l1 = distribution_options[0].state
		l2 = distribution_options[1].state

		lambdas = np.sort(np.array([l1, l2]))[::-1]

		numsamp = sample_options[0].state
		samples = sphstat.distributions.bingham(numsamp, lambdas)["points"]
		samples_array = np.vstack(samples)

		return samples_array