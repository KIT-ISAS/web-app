from abc import ABC, abstractmethod
import numpy as np
import scipy

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI

class VonMisesFibSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000)),
		]
		
	def get_name(self):
		return "Fibonacci Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state
		k = distribution_options[0].state # kappa

		gold_seq = (1+5**0.5)/2  # golden ratio

		indices = np.arange(0, sample_count)

		w = 1 + (1/k) * np.log1p((2*indices -1)/ (2*sample_count ) * np.expm1(-2 * k))
		w = np.clip(w, -1.0, 1.0) # clamp to avoid sqrt warnings due to numerical issues

		# based on https://isas.iar.kit.edu/pdf/SDFMFI23_Frisch.pdf, Forumla 39 and 40
		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]

		return x_i_f