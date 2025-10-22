from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider import Slider 
from util.selectors.slider_float import FloatSlider
import numpy as np

from model.distributions.sphere.kent.random import KentRandomSampling


class KentDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("κ (kappa)", 0.0, 10.0, 50.0),
			Slider("β (beta)", 0.0, 2.0, 25.0),
			FloatSlider("mu: Mean vector of Kent distribution: (θ)", 0, 0, np.pi),
			FloatSlider("mu: Mean vector of Kent distribution: (φ)", 0, 0, 2 * np.pi),
			FloatSlider("mu0: Mean vector of the Fisher part: (θ)", 0, np.pi, np.pi), # default values so that distibution is initially visible
			FloatSlider("mu0: Mean vector of the Fisher part: (φ)", 0, 0, 2 * np.pi),
		]
		
		self.sampling_methods = [
			KentRandomSampling()
		]

	def get_name(self):
		return "Kent (5-parameter Fisher-Bingham - FB5)"

	def get_pdf(self, distribution_options):			
		return None