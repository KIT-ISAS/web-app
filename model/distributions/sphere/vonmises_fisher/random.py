from abc import ABC, abstractmethod
import numpy as np
import scipy

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class VonMisesRandomSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000)),
		]
		
	def get_name(self):
		return "Random"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state
		kappa = distribution_options[0].state

		samples = scipy.stats.vonmises_fisher.rvs(mu=[0,0,1], kappa=kappa, size=sample_count)

		return samples