from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider_float import FloatSlider 
from util.selectors.slider import Slider
import numpy as np

from model.distributions.sphere.watson.random import WatsonRandomSampling


class WatsonDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("κ (kappa)", 0.0, 10.0, 50.0),
			FloatSlider("direction: polar angle (θ)", 0, 0, np.pi),
			FloatSlider("direction: azimuthal angle (φ)", 0, 0, 2 * np.pi),
		]
		
		self.sampling_methods = [
			WatsonRandomSampling()
		]

	def get_name(self):
		return "Watson"

	def get_pdf(self, distribution_options):			
		return None