from abc import ABC, abstractmethod
from util.selectors.slider import Slider 
import numpy as np

from model.distributions.torus.torus_distribution import TorusDistribution
from model.distributions.torus.uniform.random import TorusRandomUniformSampling

class UniformTorusDistribution(TorusDistribution):
	def __init__(self):
		self.distribution_options = []
		self.sampling_methods = [
			TorusRandomUniformSampling(),
		]

	def get_name(self):
		return "Uniform"

	def get_pdf(self, distribution_options):
		pass