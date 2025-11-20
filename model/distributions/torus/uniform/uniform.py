from abc import ABC, abstractmethod
from util.selectors.slider import Slider 
import numpy as np

from model.distributions.torus.torus_distribution import TorusDistribution
from model.distributions.torus.uniform.random import TorusRandomUniformSampling
from model.distributions.torus.uniform.fibonacci_rank_1 import TorusFibRank1UniformSampling
from model.distributions.torus.uniform.fibonacci_kronecker import TorusKroneckerUniformSampling
class UniformTorusDistribution(TorusDistribution):
	def __init__(self):
		self.distribution_options = []
		self.sampling_methods = [
			TorusRandomUniformSampling(),
			TorusFibRank1UniformSampling(),
			TorusKroneckerUniformSampling(),
		]
		

	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		scaling_factor = 5 # pdf plotted not to scale
		def pdf(x):
			N = np.shape(x)[0]
			return (1 / (4 * np.pi * np.pi)) * np.ones(N) * scaling_factor
		return pdf