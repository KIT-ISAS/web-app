import numpy as np
from model.distributions.distribution_loader import DistributionLoader
from model.distributions.torus.torus_distribution import TorusDistribution
from model.manifold import Manifold
from renderer.PlotSettings2d import PlotSettings2D

class Torus(Manifold):
	def __init__(self, resolution=100, r=1, R=3):
		self.xyz = self.generate_xyz(resolution, r, R)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.samples_2d = np.array([])
		self.distributions = DistributionLoader(TorusDistribution, "model.distributions.torus").get_distributions()

		self.r = r
		self.R = R

		axes_2d = (
			np.arange(0, 2.5 * np.pi, np.pi / 2), # 0, π/2, π, 3π/2, 2π
			["0", "π/2", "π", "3π/2", "2π"]
		)
		self.plot_settings_2d = PlotSettings2D(
			axes_2d_x=axes_2d,
			axes_2d_y=axes_2d,
			lock_aspect_ratio=True,
			periodic_x=True,
			periodic_y=True,
			periodic_x_amount=2 * np.pi,
			periodic_y_amount=2 * np.pi,
		)

	def generate_xyz(self, resolution=50, r=1, R=3):
		t = np.linspace(0, 2*np.pi, resolution)
		p = np.linspace(0, 2*np.pi, resolution)
		t,p = np.meshgrid(t,p)


		return self.t_p_to_xyz(t, p, r, R)
	
	def update_sample(self, selected_distribution, selected_sampling_method, sample_options, distribution_options):
		dist = self.distributions[selected_distribution]
		sampling_method = dist.sampling_method_dict[selected_sampling_method]
		new_sample = sampling_method.sample(sample_options, distribution_options)

		if new_sample.size == 0:
			self.samples = np.empty((0, 3), dtype=float)
			return

		x, y, z = self.t_p_to_xyz(new_sample[:,0], new_sample[:,1], self.r, self.R)

		self.samples = np.column_stack((x, y, z))
		self.samples_2d = new_sample


	@staticmethod
	def t_p_to_xyz(t, p, r=1, R=3):
		x = (R + r * np.cos(p)) * np.cos(t)
		y = (R + r * np.cos(p)) * np.sin(t)
		z = r * np.sin(p)

		return x, y, z
