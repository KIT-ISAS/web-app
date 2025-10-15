import numpy as np
from model.distributions.distribution_loader import DistributionLoader
from model.distributions.torus.torus_distribution import TorusDistribution
from model.manifold import Manifold

class Torus(Manifold):
	def __init__(self, resolution=50, r=1, R=3):
		self.xyz = self.generate_xyz(resolution, r, R)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.distributions = DistributionLoader(TorusDistribution, "model.distributions.torus").get_distributions()

		self.r = r
		self.R = R

	def generate_xyz(self, resolution=50, r=1, R=3):
		t = np.linspace(0, 2*np.pi, resolution)
		p = np.linspace(0, 2*np.pi, resolution)
		t,p = np.meshgrid(t,p)


		return self.t_p_to_xyz(t, p, r, R)
	
	def update_sample(self, selected_distribution, sample_options):
		new_sample = self.distributions[selected_distribution].sample(sample_options)

		if new_sample.size == 0:
			self.samples = np.empty((0, 3), dtype=float)
			return

		x, y, z = self.t_p_to_xyz(new_sample[:,0], new_sample[:,1], self.r, self.R)

		self.samples = np.column_stack((x, y, z))


	@staticmethod
	def t_p_to_xyz(t, p, r=1, R=3):
		x = (R + r * np.cos(p)) * np.cos(t)
		y = (R + r * np.cos(p)) * np.sin(t)
		z = r * np.sin(p)

		return x, y, z
