from abc import ABC, abstractmethod
from functools import cached_property

class Distribution(ABC):
	def __init__(self):
		self.distribution_options = []
		self.sampling_methods = []


	# Returns the name of the distribution
	@abstractmethod
	def get_name(self):
		pass

	@cached_property
	def sampling_method_dict(self):
		return {m.get_name(): m for m in self.sampling_methods}
	
	@abstractmethod
	def get_pdf(self, distribution_options):
		pass

	@property
	def info_md(self):
		return getattr(self, "_info_md", "")

	@info_md.setter
	def info_md(self, value):
		self._info_md = value