from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
import numpy as np

import pyrecest._backend
from pyrecest.backend import array
from pyrecest.distributions import BinghamDistribution

from model.distributions.sphere.bingham.random import BinghamRandomSampling


class BinghampDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("Lambda 1 (λ₁)", 0, 0, 10),
			Slider("Lambda 2 (λ₂)", 0, 0, 10),
		]
		
		self.sampling_methods = [
			BinghamRandomSampling()
		]

	def get_name(self):
		return "Bingham"

	def get_pdf(self, distribution_options):
		alpha = 0.7 # scale

		l1 = distribution_options[0].state
		l2 = distribution_options[1].state

		lambdas = np.sort(np.array([l1, l2, 0]))[::-1]
		lambdas = -lambdas
		M = np.eye(3)
		bingham_dist = BinghamDistribution(M=array(M), Z=array(lambdas))


		def pdf(x):
			bing = bingham_dist.pdf(array(x))
			max = np.max(bing)
			norm = bing / max
			norm = norm * alpha
			return norm
		return pdf