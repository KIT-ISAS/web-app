from abc import ABC, abstractmethod
from util.selectors.slider_float import FloatSlider 
import numpy as np

from model.distributions.torus.torus_distribution import TorusDistribution
from model.distributions.torus.wrapped_normal.random import TorusRandomWrappedSampling
class UniformTorusDistribution(TorusDistribution):
	def __init__(self):
		self.distribution_options = [
			FloatSlider("Sigma x (σₓ)", 0, 0.5, 5.0),
			FloatSlider("Sigma y (σᵧ)", 0, 0.5, 5.0),
			FloatSlider("Correlation (ρ)", -1, 0.1, 1),
		]
		self.sampling_methods = [
			TorusRandomWrappedSampling(),
		]
		

	def get_name(self):
		return "Wrapped Normal"

	def get_pdf(self, distribution_options):
		pass