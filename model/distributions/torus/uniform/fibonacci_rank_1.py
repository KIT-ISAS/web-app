from abc import ABC, abstractmethod
import numpy as np

from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_fib import SliderFib
from model.distributions.torus.torus_sampling_schema import TorusSamplingSchema

class TorusFibRank1UniformSampling(TorusSamplingSchema):
	def __init__(self):
		self.sample_options = [
			SliderFib("Number of Samples", 2, 34, 21, 9)
		]
		self.sampler = CylinderFibRank1UniformSampling()

	def get_name(self):
		return "Fibonacci-Rank-1 Lattice"
	
	def sample(self, sample_options, distribution_options):
		sample_count = sample_options[0].state

		t, p = self.sampler.get_rank_1(sample_count, sample_options[0].idx)

		samples = np.column_stack((t * (2* np.pi), p * (2* np.pi)))

		return samples