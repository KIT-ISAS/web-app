from abc import ABC, abstractmethod
import numpy as np

from util.selectors.silder_log import LogSlider 
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema

class TorusKroneckerUniformSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000)
		]
		self.info_md = """
		> Warning: Mapping the Kronecker lattice to the torus is not recommended in practice, as it is only periodic on one axis. 
		It is included for demonstration purposes only."""

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