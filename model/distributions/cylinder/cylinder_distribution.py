from abc import ABC, abstractmethod
from functools import cached_property
from model.distribution import Distribution


class CylinderDistribution(Distribution):
	def __init__(self):
		self.distribution_options = []
		# a list of objects that implement the cylinder_sampling_schema interface
		# that can be used with this distribution
		self.sampling_methods = []


	# Returns the name of the distribution
	@abstractmethod
	def get_name(self):
		pass

	@cached_property
	def sampling_method_dict(self):
		return {m.get_name(): m for m in self.sampling_methods}
	
	# returns a functions that takes a (N, 3) shape nparray and returns the pdf value at the points
	@abstractmethod
	def get_pdf(self, distribution_options):
		pass