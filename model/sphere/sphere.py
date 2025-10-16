import numpy as np
from model.distributions.distribution_loader import DistributionLoader
from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.manifold import Manifold
class Sphere(Manifold):
	def __init__(self, resolution=50, radius=1):
		self.xyz = self.generate_xyz(resolution, radius)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.distributions = DistributionLoader(SphereDistribution, "model.distributions.sphere").get_distributions()

	def generate_xyz(self, resolution=50, radius=1):
		phi = np.linspace(0, np.pi, resolution)
		theta = np.linspace(0, 2 * np.pi, resolution)
		phi, theta = np.meshgrid(phi, theta)

		x = radius * np.sin(phi) * np.cos(theta)
		y = radius * np.sin(phi) * np.sin(theta)
		z = radius * np.cos(phi)

		return x, y, z
	
	def update_sample(self, selected_distribution, selected_sampling_method, sample_options, distribution_options):
		dist = self.distributions[selected_distribution]
		sampling_method = dist.sampling_method_dict[selected_sampling_method]
		self.samples = sampling_method.sample(sample_options, distribution_options)

