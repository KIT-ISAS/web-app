from abc import ABC, abstractmethod
import numpy as np


from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider 

class SphereUniformFibSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000)
		]
		
	def get_name(self):
		return "Fibonacci Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		gold_seq = (1+5**0.5)/2  # golden ratio

		indices = np.arange(0, sample_count)
		
		# centered rank-1 lattice generator
		# see https://isas.iar.kit.edu/pdf/SDFMFI23_Frisch.pdf Forumla 2
		equidistant_generator = (2 * indices + 1) / (2 * sample_count)
		w = equidistant_generator

		# w is gererated in [0, 1], we need it in [-1, 1]
		w = 1 - 2 * w

		# map to sphere
		# based on https://isas.iar.kit.edu/pdf/SDFMFI23_Frisch.pdf, Forumla 39 and 40
		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0))


		return x_i_f