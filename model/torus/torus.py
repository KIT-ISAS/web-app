import numpy as np
from model.distributions.distribution_loader import DistributionLoader
from model.distributions.torus.torus_distribution import TorusDistribution

class Torus:
	def __init__(self, resolution=50, r=1, R=3):
		self.xyz = self.generate_xyz(resolution, r, R)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.distributions = DistributionLoader(TorusDistribution, "model.distributions.torus").get_distributions()

	def generate_xyz(self, resolution=50, r=1, R=3):
		t = np.linspace(0, 2*np.pi, resolution)
		p = np.linspace(0, 2*np.pi, resolution)
		t,p = np.meshgrid(t,p)


		return self.t_p_to_xyz(t, p, r, R)


	@classmethod
	def t_p_to_xyz(self, t, p, r=1, R=3):
		x = (R + r * np.cos(p)) * np.cos(t)
		y = (R + r * np.cos(p)) * np.sin(t)
		z = r * np.sin(p)

		return x, y, z
