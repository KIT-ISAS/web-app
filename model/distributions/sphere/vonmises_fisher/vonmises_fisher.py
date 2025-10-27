from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
import numpy as np
import scipy

from model.distributions.sphere.vonmises_fisher.random import VonMisesRandomSampling
from model.distributions.sphere.vonmises_fisher.fibonachi import VonMisesFibSampling

class vonMisesFisherDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("Kappa (κ)", 1, 5, 15),
		]
		
		self.sampling_methods = [
			VonMisesRandomSampling(),
			VonMisesFibSampling()
		]

	def get_name(self):
		return "von Mises-Fisher"

	def get_pdf(self, distribution_options):
		alpha = 0.7 # scale

		kappa = distribution_options[0].state
		def pdf(x):
			 
			misf = scipy.stats.vonmises_fisher.pdf(x, mu=[0,0,1], kappa=kappa)
			max = np.max(misf)

			norm = misf / max
			norm = norm * alpha
			return norm

		return pdf