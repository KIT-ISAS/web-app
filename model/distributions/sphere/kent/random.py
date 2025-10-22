from abc import ABC, abstractmethod
import numpy as np
import scipy
import sphstat

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider import Slider 
from model.sphere.sphere import Sphere


class KentRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			Slider("Number of Samples", 1, 50, 100),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		kappa = distribution_options[0].state
		beta = distribution_options[1].state
		beta = min(beta, kappa / 2) # TODO make this dynamic

		mu_theta = distribution_options[2].state
		mu_phi = distribution_options[3].state
		mu0_theta = distribution_options[4].state
		mu0_phi = distribution_options[5].state

		mu1, mu2, mu3 = Sphere.spherical_to_cartesian(mu_theta, mu_phi)
		mu0_1, mu0_2, mu0_3 = Sphere.spherical_to_cartesian(mu0_theta, mu0_phi)

		mu = [mu1, mu2, mu3]
		mu0 = [mu0_1, mu0_2, mu0_3]

		numsamp = sample_options[0].state
		samples = sphstat.distributions.kent(numsamp, kappa, beta, mu, mu0)["points"]
		samples_array = np.vstack(samples)

		return samples_array