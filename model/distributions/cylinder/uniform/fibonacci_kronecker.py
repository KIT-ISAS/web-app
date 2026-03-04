from abc import ABC, abstractmethod
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.silder_log import LogSlider 
import numpy as np
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI

class CylinderFibUniformSampling(CylinderSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000))
		]

	def get_name(self):
		return "Fibonacci-Kronecker Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		indices = np.arange(0, sample_count)
		gol = (1+5**0.5)/2
		
		# centered rank-1 lattice generator
		equidistant_generator = (2 * indices + 1) / (2 * sample_count)
		
		z = equidistant_generator
		p = (indices / gol) % 1

		return np.column_stack((p * 2 * np.pi, z * 2 * np.pi))