from abc import ABC, abstractmethod

class SamplingSchema(ABC):
	def __init__(self):
		self.sample_options = []

	# Returns the name of the sampling method
	@abstractmethod
	def get_name(self):
		pass
	
	@abstractmethod
	def sample(self, sample_options, distribution_options):
		pass

	@property
	def info_md(self):
		return getattr(self, "_info_md", "")

	@info_md.setter
	def info_md(self, value):
		self._info_md = value