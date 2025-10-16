from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
import numpy as np
import scipy

from model.distributions.sphere.vonmises_fisher.random import VonMisesRandomSampling


class vonMisesFisherDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("Kappa (κ)", 1, 5, 15),
		]
		
		self.sampling_methods = [
			VonMisesRandomSampling(),
		]

	def get_name(self):
		return "von Mises-Fisher"

	def get_pdf(self, distribution_options):
		pass