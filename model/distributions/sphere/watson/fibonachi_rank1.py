from abc import ABC, abstractmethod
from matplotlib.pyplot import grid
import numpy as np
import scipy
import scipy.integrate
import scipy.interpolate
import sphstat
from pyrecest.backend import array
from pyrecest.distributions import WatsonDistribution as WatsonDistributionPyrecest
from scipy.special import erf, erfi, erfinv

from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.slider_fib import SliderFib
from model.sphere.sphere import Sphere
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI
from model.distributions.sphere.watson.fibonachi import WatsonFibonachiSampling as wf



class WatsonFibonachiRank1Sampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderFib("Number of Samples", 3, 33, 21, 9, minus_1=True)),
		]
		self.sampler = CylinderFibRank1UniformSampling()
	
		
	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"


	def sample(self, sample_options, distribution_options):

		sample_count = sample_options[0].state + 1 # because minus_1 is true slider displays fib(n)-1
		k = distribution_options[0].state # kappa

		x, y = self.sampler.get_rank_1(sample_count, sample_options[0].idx, without_first_point=True)

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