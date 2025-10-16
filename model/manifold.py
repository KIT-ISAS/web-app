from abc import ABC, abstractmethod

class Manifold(ABC):

	# generates renderable xyz grid
	@abstractmethod
	def generate_xyz(self, *args, **kwargs):
		pass

	# updates self.sample based on selected distribution and sample options
	# also converts the sample output type to xyz coordinates
	@abstractmethod
	def update_sample(self,  selected_distribution, sample_options):
		pass

	def generate_trisurf(self, pdf, *args, **kwargs):
		pass