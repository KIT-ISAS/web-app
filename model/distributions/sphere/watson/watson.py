from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider_float import FloatSlider 
from util.selectors.slider import Slider
import numpy as np
import pyrecest._backend
from pyrecest.backend import array
from pyrecest.distributions import WatsonDistribution as WatsonDistributionPyrecest

from model.distributions.sphere.watson.random_sampling import WatsonRandomSampling
from model.distributions.sphere.watson.fibonachi import WatsonFibonachiSampling
from model.distributions.sphere.watson.cartesian import WatsonCartesianSampling
from model.distributions.sphere.watson.fibonachi_rank1 import WatsonFibonachiRank1Sampling			


class WatsonDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("κ (kappa)", -50, 10.0, 50.0),
		]
		
		self.sampling_methods = [
			WatsonRandomSampling(),
			WatsonFibonachiSampling(),
			WatsonCartesianSampling(),
			WatsonFibonachiRank1Sampling(),
		]

	def get_name(self):
		return "Watson"

	def get_pdf(self, distribution_options):
		alpha = 0.5 # scale			
		kappa = distribution_options[0].state
		mu = array([0.0, 0.0, 1.0])

		watson_dist = WatsonDistributionPyrecest(mu=mu, kappa=kappa)

		def pdf(x):
			wts = watson_dist.pdf(array(x))
			max = np.max(wts)
			norm = wts / max
			norm = norm * alpha
			return norm
		return pdf