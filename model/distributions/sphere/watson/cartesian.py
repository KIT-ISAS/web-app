from abc import ABC, abstractmethod
import numpy as np
import scipy
from scipy.special import erf, erfi, erfinv


from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from model.distributions.sphere.watson.fibonachi import WatsonFibonachiSampling as wf
from util.selectors.slider_square import SliderSquare
from util.cartesian_util import CartesianUtil as cu
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class WatsonCartesianSampling(SphereSamplingSchema):
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
		# map cartesian grid to watson, using inverse cdf closed form, see fibonachi.py for reference

		# for kappa = 0, w=cos(theta) is uniform in [−1,1] and phi is uniform in [0,2pi]
		# this is contrary to uniform_samping where theta is uniform in [0, pi] and phi in [0, 2pi]


		sample_count = sample_options[0].state
		n = int(np.sqrt(sample_count))
		k = distribution_options[0].state # kappa

		grid = cu.generate_cartesian_grid(n, (1, 1))
		x, y = grid[:,0], grid[:,1]
		x = 2*x -1  # map x from [0,1] to [-1, 1]
		phi = 2 * np.pi * y  # azimuthal angle, [0, 2pi] uniform

		if k > 0:
			w = 1 / (np.sqrt(k)) * wf.erfi_inv( x * erfi(np.sqrt(k)) )
		elif k < 0:
			la = -k
			w = 1 / (np.sqrt(la)) * erfinv( x * erf(np.sqrt(la)) )
		elif k == 0:
			w = x


		w = np.clip(w, -1.0, 1.0) # clamp to avoid sqrt warnings due to numerical issues

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( phi)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( phi)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f

		
