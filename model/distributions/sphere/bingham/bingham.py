from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from util.selectors.slider_float import FloatSlider 
import numpy as np

from model.distributions.sphere.bingham.random import BinghamRandomSampling


class BinghampDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			FloatSlider("Lambda 1 (λ₁)", -0.49, 0, 0),
			FloatSlider("Lambda 2 (λ₂)", -0.49, 0, 0),
		]
		
		self.sampling_methods = [
			BinghamRandomSampling()
		]

	def get_name(self):
		return "Bingham"

	def get_pdf(self, distribution_options):			
		return None