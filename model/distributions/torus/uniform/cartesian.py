import numpy as np

from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema
from util.selectors.slider_square import SliderSquare
from util.cartesian_util import CartesianUtil as cu
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class TorusCartesianUniformSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderSquare("Number of Samples", 4, 64, 100, 4))
		]
		self.info_md = """
		> Warning: Using the Cartesian Grid is not recomended in practise, as it yields bad results. 
		It is included for demonstration purposes only."""

	def get_name(self):
		return "Cartesian Grid"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		n = int(np.sqrt(sample_count))
		return cu.generate_cartesian_grid(n, (2 * np.pi, 2 * np.pi))