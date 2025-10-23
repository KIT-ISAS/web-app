import numpy as np
import numpy as np
from scipy.spatial import Delaunay
import plotly.figure_factory as ff

from model.distributions.distribution_loader import DistributionLoader
from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.manifold import Manifold

class Sphere(Manifold):
	def __init__(self, resolution=50, radius=1):
		self.xyz = self.generate_xyz(resolution, radius)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.distributions = DistributionLoader(SphereDistribution, "model.distributions.sphere").get_distributions()

		self.dist_cache = {}

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


	def generate_mesh(self, pdf, resolution=30, radius=1, alpha=0.5):
		phi = np.linspace(0, np.pi, resolution)
		theta = np.linspace(0, 2 * np.pi, resolution)
		phi, theta = np.meshgrid(phi, theta)

		phi = phi.flatten()
		theta = theta.flatten()

		x = radius * np.sin(phi) * np.cos(theta)
		y = radius * np.sin(phi) * np.sin(theta)
		z = radius * np.cos(phi)

		points2D = np.vstack([phi,theta]).T
		tri = Delaunay(points2D)
		simplices = tri.simplices

		xyz = np.column_stack((x, y, z))
		dens = pdf(xyz)

		# clamp color function just below max
		# even though colorscale is not shown, this prevents ff.create_trisurf from crashing due to an overflow
		def cf(xi, yi, zi, zmin=np.min(z), zmax=np.max(z)):
			if zi > zmax:
				zi = np.nextafter(zmax, zmin)
			return zi

		
		# extrude by multiplying by 1 + dens * alpha
		# not to scale, but the alpha makes the density function look more clearly
		xyz_extruded =  xyz * (1 + alpha * dens[:, np.newaxis])
		x, y, z = xyz_extruded[:,0], xyz_extruded[:,1], xyz_extruded[:,2]

		fig = ff.create_trisurf(x=x, y=y, z=z,
								simplices=simplices,
								show_colorbar=False,
								color_func=cf
								)
		fig.data[0].update(
			opacity=0,
			color='black'
		)

		
		return fig.data[1].x, fig.data[1].y, fig.data[1].z
	
	@staticmethod
	def spherical_to_cartesian(theta, phi, r=1):
		x = r * np.sin(theta) * np.cos(phi)
		y = r * np.sin(theta) * np.sin(phi)
		z = r * np.cos(theta)

		return x, y, z

