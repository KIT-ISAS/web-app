from abc import ABC, abstractmethod
from util.selectors.slider_float import FloatSlider 
import numpy as np

from model.distributions.cylinder.cylinder_distribution import CylinderDistribution
from model.distributions.cylinder.partially_wraped_normal.random import CylinderRandomPWNSampling


class PartiallyWrappedNormalDistribution(CylinderDistribution):
	def __init__(self):
		self.distribution_options = [
			FloatSlider("Sigma x (σₓ)", 0, 0.5, 5.0),
			FloatSlider("Sigma y (σᵧ)", 0, 0.5, 1.0),
			FloatSlider("Correlation (ρ)", -1, 0.1, 1),
		]
		self.sampling_methods = [
			CylinderRandomPWNSampling(),
		]

	def get_name(self):
		return "Partially Wrapped Normal"

	def get_pdf(self, distribution_options):
		pass