from abc import ABC, abstractmethod
import numpy as np
import scipy
import sphstat

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider import Slider 
from model.sphere.sphere import Sphere


class WatsonRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 1, 50, 100),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		kappa = distribution_options[0].state
		
		theta = 0 # can be hardcoded because the user can just turn the sphere
		phi = 0

		numsamp = sample_options[0].state

		lamb, mu, nu = Sphere.spherical_to_cartesian(theta, phi)

		samples = sphstat.distributions.watson(numsamp, lamb, mu, nu, kappa)["points"]
		samples_array = np.vstack(samples)

		return samples_array