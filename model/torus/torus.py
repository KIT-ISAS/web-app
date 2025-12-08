import numpy as np
import plotly.figure_factory as ff
from scipy.spatial import Delaunay

from model.distributions.distribution_loader import DistributionLoader
from model.distributions.torus.torus_distribution import TorusDistribution
from model.manifold import Manifold
from renderer.plot_settings_2d import PlotSettings2D
from model.distributions.cylinder.uniform.fibonacci_rank_1 import CylinderFibRank1UniformSampling
from util.selectors.slider_fib import SliderFib

class Torus(Manifold):
	def __init__(self, resolution=100, r=1, R=3):
		self.xyz = self.generate_xyz(resolution, r - 0.01, R - 0.01) # slightly smaller to avoid artifacts from mesh

		self.distributions = DistributionLoader(TorusDistribution, "model.distributions.torus").get_distributions()

		self.r = r
		self.R = R

		self.mesh_xyz = self._init_mesh()

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
			x_title="t",
			y_title="p",
			reverse_x_y_axis=True, # x is p, y is t
			color_location=(0,0,2*np.pi, 2*np.pi),
		)

	def generate_xyz(self, resolution=50, r=1, R=3):
		t = np.linspace(0, 2*np.pi, resolution)
		p = np.linspace(0, 2*np.pi, resolution)
		t,p = np.meshgrid(t,p)


		return self.t_p_to_xyz(t, p, r, R)
	
	def pdf_2d(self, xy, pdf):
		x, y, z = self.t_p_to_xyz(xy[:,0], xy[:,1], self.r, self.R)
		return pdf(np.column_stack((x, y, z)))

	
	def update_sample(self, selected_distribution, selected_sampling_method, sample_options, distribution_options):
		dist = self.distributions[selected_distribution]
		sampling_method = dist.sampling_method_dict[selected_sampling_method]
		new_sample = sampling_method.sample(sample_options, distribution_options)

		if (new_sample is None) or new_sample.size == 0:
			samples = np.empty((0, 3), dtype=float)
			samples_2d = np.empty((0, 2), dtype=float)
			return (samples, samples_2d)

		x, y, z = self.t_p_to_xyz(new_sample[:,0], new_sample[:,1], self.r, self.R)

		samples = np.column_stack((x, y, z))
		samples_2d = new_sample
		return (samples, samples_2d)


	@staticmethod
	def t_p_to_xyz(t, p, r=1, R=3):
		x = (R + r * np.cos(p)) * np.cos(t)
		y = (R + r * np.cos(p)) * np.sin(t)
		z = r * np.sin(p)

		return x, y, z
	
	@staticmethod
	def xyz_to_t_p(x, y, z, r=1, R=3):
		t = np.arctan2(y, x)
		p = np.arctan2(z, np.sqrt(x**2 + y**2) - R)
		return t, p
	
	
	
	def generate_mesh(self, pdf, alpha=1):
		#return self.mesh_xyz[:,0], self.mesh_xyz[:,1], self.mesh_xyz[:,2]

		# mesh_xyz has nans for line segments, mask before passing to pdf
		mask = np.all(np.isfinite(self.mesh_xyz), axis=-1)
		dens = pdf(self.mesh_xyz[mask])

		xyz_extruded = np.full_like(self.mesh_xyz, np.nan, dtype=float) # full of nans
		tp = self.xyz_to_t_p(self.mesh_xyz[mask][:,0], self.mesh_xyz[mask][:,1], self.mesh_xyz[mask][:,2], self.r, self.R)
		xyz_new = self.t_p_to_xyz(tp[0], tp[1], self.r * (1 + alpha * dens), self.R)
		xyz_extruded[mask] =  np.stack(xyz_new, axis=1)
		return xyz_extruded[:,0], xyz_extruded[:,1], xyz_extruded[:,2]
	

	def _init_mesh(self, resolution=(4181, 19)):
		
		#tp = CylinderFibRank1UniformSampling.sample(None, [SliderFib("Number of Samples", 10, resolution[0], resolution[0], resolution[1])] , [])
		k = resolution[1]
		samp_count = resolution[0]
		t, p = CylinderFibRank1UniformSampling.get_rank_1(samp_count, k)
		tp = np.column_stack((t * 2 * np.pi, p * 2 * np.pi))

		x, y, z = self.t_p_to_xyz(tp[:,0], tp[:,1], self.r)

		

		def simplices_with_mask(_tp):
			_simplices = Delaunay(_tp).simplices

			# only inner, avoid pi/4 border
			ok_mask = (_tp[:, 0] > np.pi / 4) & (_tp[:, 0] < 7 * np.pi / 4) & (_tp[:, 1] > np.pi / 4) & (_tp[:, 1] < 7 * np.pi / 4)
			ok_idx = np.where(ok_mask)[0]

			# throw away all triangles around the border
			good_vertices = np.isin(_simplices, ok_idx)
			good_triangles = good_vertices.any(axis=1)
			_simplices = _simplices[good_triangles]
			return _simplices


		# shift p by pi/2 and cluster 4 quadrants with overlap
		tp1  = np.copy(tp)
		tp1[:,0] = (tp1[:,0]+(np.pi/2)) % (2 * np.pi)
		tp1[:,1] = (tp1[:,1]+(np.pi/2)) % (2 * np.pi)
		simplices_1 = simplices_with_mask(tp1)

		tp2  = np.copy(tp)
		tp2[:,0] = (tp2[:,0]+(np.pi/2)) % (2 * np.pi)
		tp2[:,1] = (tp2[:,1]-(np.pi/2)) % (2 * np.pi)
		simplices_2 = simplices_with_mask(tp2)

		tp3 = np.copy(tp)
		tp3[:,0] = (tp3[:,0]-(np.pi/2)) % (2 * np.pi)
		tp3[:,1] = (tp3[:,1]-(np.pi/2)) % (2 * np.pi)
		simplices_3 = simplices_with_mask(tp3)

		tp4 = np.copy(tp)
		tp4[:,0] = (tp4[:,0]-(np.pi/2)) % (2 * np.pi)
		tp4[:,1] = (tp4[:,1]+(np.pi/2)) % (2 * np.pi)
		simplices_4 = simplices_with_mask(tp4)

		# merge all four quadrants
		simplices_merged = np.vstack((simplices_1, simplices_2, simplices_3, simplices_4))
		simplices_merged = np.unique(simplices_merged, axis=0)

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

