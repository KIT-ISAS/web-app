from abc import ABC, abstractmethod
import numpy as np

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_fib import SliderFib
from model.sphere.sphere import Sphere
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI


class SphereFibRank1UniformSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(SliderFib("Number of Samples", 2, 34, 21, 9))
		]
		self.sampler = CylinderFibRank1UniformSampling()
		
	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		t, p = self.sampler.get_rank_1(sample_count, sample_options[0].idx)

		z = 1 - 2 * t # uniform in [-1, 1]
		phi = p * (2 * np.pi)
		x = np.sqrt(1 - z**2) * np.cos(phi)
		y = np.sqrt(1 - z**2) * np.sin(phi)


		return np.column_stack((x, y, z))