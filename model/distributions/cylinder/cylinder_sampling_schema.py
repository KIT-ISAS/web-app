from abc import ABC, abstractmethod

class CylinderSamplingSchema(ABC):
	def __init__(self):
		self.sample_options = []

	# Returns the name of the sampling method
	@abstractmethod
	def get_name(self):
		pass
	
	# returns samples as a numpy array of shape (n, 2)
	# where (2)	are the parameters (p, z) (angle, height) on the torus 
	@abstractmethod
	def sample(self, sample_options, distribution_options):
		pass