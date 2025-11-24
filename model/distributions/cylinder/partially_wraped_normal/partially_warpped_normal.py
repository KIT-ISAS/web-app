from util.selectors.slider_float import FloatSlider 
import numpy as np
from scipy.stats import multivariate_normal


from model.distributions.cylinder.cylinder_distribution import CylinderDistribution
from model.distributions.cylinder.partially_wraped_normal.random import CylinderRandomPWNSampling
from model.cylinder.cylinder import Cylinder

class PartiallyWrappedNormalDistribution(CylinderDistribution):
	def __init__(self):
		self.distribution_options = [
			FloatSlider("Sigma x (σₓ)", 0, 0.5, 5.0),
			FloatSlider("Sigma y (σᵧ)", 0, 0.5, 1.0),
			FloatSlider("Correlation (ρ)", -1, 0.1, 1),
		]
		self.sampling_methods = [
			CylinderRandomPWNSampling(),
		]

	def get_name(self):
		return "Partially Wrapped Normal"

	def get_pdf(self, distribution_options):
		sigma_x = distribution_options[0].state
		sigma_y = distribution_options[1].state
		correlation = distribution_options[2].state

		Cov = np.array([
			[sigma_x**2, correlation * sigma_x * sigma_y],
			[correlation * sigma_x * sigma_y, sigma_y**2]
		])

		mean = np.array([np.pi, np.pi])

		dist = multivariate_normal(mean=mean, cov=Cov)

		def pdf(x):
			alpha = 0.7 # scale

			p, z = Cylinder.xyz_to_p_z(x[:,0], x[:,1], x[:,2])
			p_z = np.column_stack((p, z))

			# wrap until 3 * sigma_x
			k = int(np.ceil(3 * sigma_x / (2 * np.pi)))

			total_pdf = np.zeros(p_z.shape[0])
			for i in range(-k, k+1):
				shifted_samples = np.column_stack((p_z[:,0] + i * 2 * np.pi, p_z[:,1]))
				total_pdf += dist.pdf(shifted_samples)

			max = np.max(total_pdf)

			norm = total_pdf / max
			norm = norm * alpha
			return norm

		return pdf
