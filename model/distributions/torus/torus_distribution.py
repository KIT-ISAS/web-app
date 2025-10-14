from abc import ABC, abstractmethod

class TorusDistribution(ABC):
	def __init__(self):
		self.sample_options = []
		self.distribution_options = []

	# Returns the name of the distribution
	@abstractmethod
	def get_name(self):
		pass
	
	# returns samples as a numpy array of shape (n, 2)
	# where (2)	are the parameters (t, p) on the torus
	@abstractmethod
	def sample(self, sample_options):
		pass

	@abstractmethod
	def generate_mesh(self, distribution_options):
		pass