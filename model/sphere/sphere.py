import numpy as np
import numpy as np
from scipy.spatial import ConvexHull
import plotly.figure_factory as ff

from model.distributions.distribution_loader import DistributionLoader
from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.manifold import Manifold
from model.distributions.sphere.uniform.fibonachi_lattice import SphereUniformFibSampling
from util.selectors.slider import Slider

class Sphere(Manifold):
	def __init__(self, resolution=200, radius=0.999):
		self.xyz = self.generate_xyz(resolution, radius)

		self.distributions = DistributionLoader(SphereDistribution, "model.distributions.sphere").get_distributions()


		self.mesh_xyz = self._init_mesh()

		

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
		return (sampling_method.sample(sample_options, distribution_options), None)


	def generate_mesh(self, pdf, alpha=1):
		# mesh_xyz has nans for line segments, mask before passing to pdf
		mask = np.all(np.isfinite(self.mesh_xyz), axis=-1)
		dens = pdf(self.mesh_xyz[mask])

		xyz_extruded = np.full_like(self.mesh_xyz, np.nan, dtype=float) # full of nans

		xyz_extruded[mask] =  self.mesh_xyz[mask] * (1 + alpha * dens[:, np.newaxis])
		return xyz_extruded[:,0], xyz_extruded[:,1], xyz_extruded[:,2]

	def _init_mesh(self, resolution=3000):
		xyz = SphereUniformFibSampling.sample(None, [Slider("Number of Samples", 10, resolution, resolution)] , [])
		x, y, z = xyz[:,0], xyz[:,1], xyz[:,2]

		hull = ConvexHull(xyz)
		simplices = hull.simplices

		def cf(xi, yi, zi, zmin=np.min(z), zmax=np.max(z)):
			if zi > zmax:
				zi = np.nextafter(zmax, zmin)
			return zi

		fig = ff.create_trisurf(x=x, y=y, z=z,
								simplices=simplices,
								show_colorbar=False,
								color_func=cf
								)
		
		arr =  np.column_stack((fig.data[1].x, fig.data[1].y, fig.data[1].z))
		return np.where(arr == None, np.nan, arr).astype(float) # line segments have None in them, put them to nan so we can do mult later
	
	@staticmethod
	def spherical_to_cartesian(theta, phi, r=1):
		x = r * np.sin(theta) * np.cos(phi)
		y = r * np.sin(theta) * np.sin(phi)
		z = r * np.cos(theta)

		return x, y, z

