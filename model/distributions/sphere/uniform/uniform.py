from abc import ABC, abstractmethod
import numpy as np

from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.distributions.sphere.uniform.random import SphereUniformRandomSampling
from model.distributions.sphere.uniform.fibonachi_lattice import SphereUniformFibSampling
from model.distributions.sphere.uniform.fibonacci_rank_1 import SphereFibRank1UniformSampling

class SphereUniformDistribution(SphereDistribution):
	def __init__(self):		
		self.distribution_options = []
		self.sampling_methods = [
			SphereUniformRandomSampling(),
			SphereUniformFibSampling(),
			SphereFibRank1UniformSampling(),
		]


	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		# https://math.stackexchange.com/questions/2315341/how-to-write-a-proper-definition-of-the-uniform-distribution-on-unit-sphere
		def pdf(x):
			N = np.shape(x)[0]
			return (1/ (4*np.pi)) * np.ones(N)
		return pdf