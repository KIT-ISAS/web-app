from abc import ABC, abstractmethod
from util.selectors.slider import Slider 
import numpy as np

from model.distributions.cylinder.cylinder_distribution import CylinderDistribution
from model.distributions.cylinder.uniform.random import CylinderRandomUniformSampling
from model.distributions.cylinder.uniform.fibonacci_kronecker import CylinderFibUniformSampling

class UniformCylinderDistribution(CylinderDistribution):
	def __init__(self):
		self.distribution_options = []
		self.sampling_methods = [
			CylinderRandomUniformSampling(),
			CylinderFibUniformSampling(),
		]

	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		pass