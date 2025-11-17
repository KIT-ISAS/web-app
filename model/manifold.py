from abc import ABC, abstractmethod

class Manifold(ABC):
	# optional initial settings for 3d camera
	@property
	def camera_settings_3d(self):
		return getattr(self, "_camera_settings_3d", None)

	@camera_settings_3d.setter
	def camera_settings_3d(self, value):
		self._camera_settings_3d = value

	# optional, setting for if the manifold supports 2d plotting
	@property
	def plot_settings_2d(self):
		return getattr(self, "_plot_settings_2d", None)

	@plot_settings_2d.setter
	def plot_settings_2d(self, value):
		self._plot_settings_2d = value

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