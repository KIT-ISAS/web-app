from abc import ABC, abstractmethod
import numpy as np
import scipy
import sphstat
from kent_distribution import kent2

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider
from model.sphere.sphere import Sphere


class KentRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		kappa = distribution_options[0].state
		beta = distribution_options[1].state
		beta = min(beta, kappa / 2) # TODO make this dynamic

		kent = kent2([1, 0, 0], [0, 1, 0], [0, 0, 1], kappa, beta)
		numsamp = sample_options[0].state
		samp = kent.rvs(n_samples=numsamp)
		xyz = samp[:, [2, 1, 0]] # samples get returned in z,y,x order
		return xyz