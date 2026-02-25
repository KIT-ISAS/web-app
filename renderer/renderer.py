from abc import ABC, abstractmethod

class Renderer(ABC):

	"""
	returns a tuple of the a list of settings components (eg. for the sidebar) and a list of plot components
	"""
	@abstractmethod
	def get_layout_components(self):
		pass