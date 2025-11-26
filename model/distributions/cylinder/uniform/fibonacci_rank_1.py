from abc import ABC, abstractmethod
from model.distributions.cylinder.cylinder_sampling_schema import CylinderSamplingSchema
from util.selectors.slider_fib import SliderFib
import numpy as np	
import sympy as sp
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI

class CylinderFibRank1UniformSampling(CylinderSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderFib("Number of Samples", 2, 34, 21, 9))
		]

	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state
		k = sample_options[0].idx

		z, p = self.get_rank_1(sample_count, k)

		return np.column_stack((p * 2 * np.pi, z * 2 * np.pi))
	
	@staticmethod
	def get_rank_1(sample_count, k):
		indices = np.arange(0, sample_count)
		
		# centered rank-1 lattice
		F_k = int(sp.fibonacci(k - 1))
		F_k_p_1 = sample_count  # int(sp.fibonacci(k))
		
		z = (indices * (1/F_k_p_1) + (1/(2*F_k_p_1)) ) % 1
		p = (indices * (F_k/F_k_p_1) + (1/(2*F_k_p_1)) ) % 1

		return z, p