from abc import ABC, abstractmethod
from model.sampling_schema import SamplingSchema

class TorusSamplingSchema(SamplingSchema):
	def __init__(self):
		self.sample_options = []

	# Returns the name of the sampling method
	@abstractmethod
	def get_name(self):
		pass
	
	# returns samples as a numpy array of shape (n, 2)
	# where (2)	are the parameters (t, p) on the torus
	@abstractmethod
	def sample(self, sample_options, distribution_options):
		pass