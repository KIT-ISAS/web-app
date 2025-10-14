from abc import ABC, abstractmethod

class TorusDistribution(ABC):
	def __init__(self):
		self.sample_options = []
		self.distribution_options = []

	# Returns the name of the distribution
	@abstractmethod
	def get_name(self):
		pass
	
	# returns samples as a TODO
	@abstractmethod
	def sample(self, sample_options):
		pass

	@abstractmethod
	def generate_mesh(self, distribution_options):
		pass