import numpy as np
from scipy.spatial import ConvexHull
import plotly.figure_factory as ff
from scipy.spatial import Delaunay


from model.distributions.distribution_loader import DistributionLoader
from model.distributions.cylinder.cylinder_distribution import CylinderDistribution
from model.manifold import Manifold
from renderer.PlotSettings2d import PlotSettings2D
from model.distributions.cylinder.uniform.fibonacci_kronecker import CylinderFibUniformSampling
from util.selectors.slider import Slider

class Cylinder(Manifold):
	def __init__(self, resolution=100, r=1):
		self.xyz = self.generate_xyz(resolution, r)
		self.mesh = np.array([])
		self.samples = np.array([])
		self.samples_2d = np.array([])
		self.distributions = DistributionLoader(CylinderDistribution, "model.distributions.cylinder").get_distributions()

		self.r = r
		self.mesh_xyz = self._init_mesh()

		axes_2d = (
			np.arange(0, 2.5 * np.pi, np.pi / 2), # 0, π/2, π, 3π/2, 2π
			["0", "π/2", "π", "3π/2", "2π"]
		)
		self.plot_settings_2d = PlotSettings2D(
			axes_2d_x=axes_2d,
			axes_2d_y=axes_2d,
			lock_aspect_ratio=False,
			periodic_x=True,
			periodic_y=False,
			periodic_x_amount=2 * np.pi,
			x_title="p",
			y_title="z",
			reverse_x_y_axis=False,
		)

		self.camera_settings_3d = dict(
			eye=dict(x=2, y=2, z=2),
			center=dict(x=0, y=0, z=0),
		)

	def generate_xyz(self, resolution=50, r=1):
		p = np.linspace(0, 2*np.pi, resolution)
		z = np.linspace(0, 2*np.pi, resolution)
		t,p = np.meshgrid(p,z)


		return self.p_z_to_xyz(t, p, r)
	
	def update_sample(self, selected_distribution, selected_sampling_method, sample_options, distribution_options):
		dist = self.distributions[selected_distribution]
		sampling_method = dist.sampling_method_dict[selected_sampling_method]
		new_sample = sampling_method.sample(sample_options, distribution_options)

		if (new_sample is None) or new_sample.size == 0:
			self.samples = np.empty((0, 3), dtype=float)
			return

		x, y, z = self.p_z_to_xyz(new_sample[:,0], new_sample[:,1], self.r)

		self.samples = np.column_stack((x, y, z))
		self.samples_2d = new_sample


	@staticmethod
	def p_z_to_xyz(p, z, r=1):
		x = r * np.cos(p)
		y = r * np.sin(p)
		z = r * z

		return x, y, z
	
	def generate_mesh(self, pdf, alpha=1):
		# mesh_xyz has nans for line segments, mask before passing to pdf
		mask = np.all(np.isfinite(self.mesh_xyz), axis=-1)
		dens = pdf(self.mesh_xyz[mask]) # only extrude on p, dont change z

		xyz_extruded = np.full_like(self.mesh_xyz, np.nan, dtype=float) # full of nans

		xyz_extruded[..., :2][mask] =  self.mesh_xyz[..., :2][mask] * (1 + alpha * dens[:, np.newaxis])
		xyz_extruded[..., 2][mask] = self.mesh_xyz[..., 2][mask] # z unchanged
		return xyz_extruded[:,0], xyz_extruded[:,1], xyz_extruded[:,2]
	
	def _init_mesh(self, resolution=3000):
		pz = CylinderFibUniformSampling.sample(None, [Slider("Number of Samples", 10, resolution, resolution)] , [])
		pz[:, 1] = -0.1 + (pz[:, 1]) * 1.1 # extend slightly beyond [0, 2pi] so the top and bottom looks better
		x, y, z = self.p_z_to_xyz(pz[:,0], pz[:,1], self.r)

		simplices = Delaunay(pz).simplices
		ok_mask = (pz[:, 0] > np.pi / 4) & (pz[:, 0] < 7 * np.pi / 4) # ugly seam
		ok_idx = np.where(ok_mask)[0]

		# throw away all triangles around the seam
		good_vertices = np.isin(simplices, ok_idx)
		good_triangles = good_vertices.any(axis=1)
		simplices = simplices[good_triangles]


		# shift p by pi and throw away triangles at other seam, that is at the opposite side
		pz2  = np.copy(pz)
		pz2[:,0] = (pz2[:,0]+np.pi) % (2 * np.pi)

		simplices_2 = Delaunay(pz2).simplices
		ok_mask_2 = (pz2[:, 0] > np.pi / 4) & (pz2[:, 0] < 7 * np.pi / 4) # ugly seam
		ok_idx_2 = np.where(ok_mask_2)[0]

		good_vertices_2 = np.isin(simplices_2, ok_idx_2)
		good_triangles_2 = good_vertices_2.any(axis=1)
		simplices_2 = simplices_2[good_triangles_2]

		# merge both halves
		simplices_merged = np.vstack((simplices, simplices_2))
		simplices_merged = np.unique(simplices_merged, axis=0)

		# throw away points at bottom so they dont stretch across
		eps = 1e-2
		ok_mask_no_across = (pz[:, 1] > 0 + eps) & (pz[:, 1] < (2 * np.pi - eps))
		ok_idx_no_across = np.where(ok_mask_no_across)[0]
		good_vertices_no_across = np.isin(simplices_merged, ok_idx_no_across)
		good_triangles_no_across = good_vertices_no_across.all(axis=1)
		simplices_merged = simplices_merged[good_triangles_no_across]



		def cf(xi, yi, zi, zmin=np.min(z), zmax=np.max(z)):
			if zi > zmax:
				zi = np.nextafter(zmax, zmin)
			return zi

		fig = ff.create_trisurf(x=x, y=y, z=z,
								simplices=simplices_merged,
								show_colorbar=False,
								color_func=cf
								)
		
		arr =  np.column_stack((fig.data[1].x, fig.data[1].y, fig.data[1].z))
		return np.where(arr == None, np.nan, arr).astype(float) # line segments have None in them, put them to nan so we can do mult later
