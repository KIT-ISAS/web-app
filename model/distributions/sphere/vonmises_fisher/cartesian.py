from abc import ABC, abstractmethod
import numpy as np
import scipy

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider_square import SliderSquare
from util.cartesian_util import CartesianUtil as cu

class VonMisesCartesianSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			SliderSquare("Number of Samples", 4, 64, 100, 4)
		]
		self.info_md = """
		> Warning: Using the Cartesian Grid is not recomended in practise, as it yields bad results. 
		It is included for demonstration purposes only."""

	def get_name(self):
		return "Cartesian Grid"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state
		n = int(np.sqrt(sample_count))
		k = distribution_options[0].state # kappa

		grid = cu.generate_cartesian_grid(n, (1, 1))
		x, y = grid[:,0], grid[:,1]
		phi = 2 * np.pi * y  # azimuthal angle, [0, 2pi] uniform

		w = 1 + (1/k) * np.log1p(x * np.expm1(-2 * k))
		w = np.clip(w, -1.0, 1.0) # clamp to avoid sqrt warnings due to numerical issues

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( phi)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( phi)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f

		
