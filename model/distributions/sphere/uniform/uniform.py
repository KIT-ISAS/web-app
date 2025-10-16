from abc import ABC, abstractmethod
from util.selectors.slider import Slider 
import numpy as np

from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.distributions.sphere.uniform.random import SphereUniformRandomSampling


class SphereUniformDistribution(SphereDistribution):
	def __init__(self):		
		self.distribution_options = []
		self.sampling_methods = [
			SphereUniformRandomSampling(),
		]


	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		# https://math.stackexchange.com/questions/2315341/how-to-write-a-proper-definition-of-the-uniform-distribution-on-unit-sphere
		def pdf(x):
			return 1/ (4*np.pi)
		return pdf