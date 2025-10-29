from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider_float import FloatSlider 
import numpy as np

import pyrecest._backend
from pyrecest.backend import array
from pyrecest.distributions import BinghamDistribution

from model.distributions.sphere.bingham.random import BinghamRandomSampling


class BinghampDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			FloatSlider("Lambda 1 (λ₁)", 0, 0, 10),
			FloatSlider("Lambda 2 (λ₂)", 0, 0, 10),
		]
		
		self.sampling_methods = [
			BinghamRandomSampling()
		]

	def get_name(self):
		return "Bingham"

	def get_pdf(self, distribution_options):			
		l1 = distribution_options[0].state
		l2 = distribution_options[1].state

		lambdas = np.sort(np.array([l1, l2, 0]))[::-1]
		lambdas = -lambdas
		print(lambdas)
		M = np.eye(3)
		bingham_dist = BinghamDistribution(M=array(M), Z=array(lambdas))


		def pdf(x):
			return bingham_dist.pdf(array(x))
		return pdf