from abc import ABC, abstractmethod
from util.selectors.slider import Slider 
import numpy as np

from model.distributions.cylinder.cylinder_distribution import CylinderDistribution
from model.distributions.cylinder.uniform.random import CylinderRandomUniformSampling
from model.distributions.cylinder.uniform.fibonacci_kronecker import CylinderFibUniformSampling
from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
class UniformCylinderDistribution(CylinderDistribution):
	def __init__(self):
		self.distribution_options = []
		self.sampling_methods = [
			CylinderRandomUniformSampling(),
			CylinderFibUniformSampling(),
			CylinderFibRank1UniformSampling(),
		]

	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		scaling_factor = 5 # pdf plotted not to scale
		def pdf(x):
			N = np.shape(x)[0]
			return (1 / (4 * np.pi * np.pi)) * np.ones(N) * scaling_factor
		return pdf