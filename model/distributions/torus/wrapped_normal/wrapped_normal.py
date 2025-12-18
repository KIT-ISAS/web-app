import numpy as np
from scipy.stats import multivariate_normal

from util.selectors.slider_float import FloatSlider 
from util.selectors.slider_pi import PiSlider
from model.distributions.torus.torus_distribution import TorusDistribution
from model.distributions.torus.wrapped_normal.random import TorusRandomWrappedSampling
from model.distributions.torus.wrapped_normal.fibonacci import TorusFibRank1WNSampling
from model.distributions.torus.wrapped_normal.fibonacci_kronecker import TorusFibKroneckerWNSampling
from model.distributions.torus.wrapped_normal.cartesian import TorusFibCartWNSampling
from model.distributions.torus.wrapped_normal.frolov import CFrolovWNSampling
from model.distributions.torus.wrapped_normal.improved_frolov import IFrolovWNSampling
from model.torus.torus import Torus
class WrappedNormalTorusDistribution(TorusDistribution):
	def __init__(self):
		self.distribution_options = [
			PiSlider("Mean p (μₚ)", 0, 1, 2),
			PiSlider("Mean t (μₜ)", 0, 1, 2),
			FloatSlider("Sigma p (σₚ)", 0, 0.5, 5.0),
			FloatSlider("Sigma t (σₜ)", 0, 0.5, 5.0),
			FloatSlider("Correlation (ρ)", -1, 0.1, 1),
		]
		self.sampling_methods = [
			TorusRandomWrappedSampling(),
			TorusFibRank1WNSampling(),
			TorusFibKroneckerWNSampling(),
			TorusFibCartWNSampling(),
			CFrolovWNSampling(),
			IFrolovWNSampling(),
		]
		

	def get_name(self):
		return "Wrapped Normal"

	def get_pdf(self, distribution_options):
		mean_x = distribution_options[0].state
		mean_y = distribution_options[1].state
		sigma_t = distribution_options[2].state
		sigma_p = distribution_options[3].state
		correlation = distribution_options[4].state

		Cov = np.array([
			[sigma_t**2, correlation * sigma_t * sigma_p],
			[correlation * sigma_t * sigma_p, sigma_p**2]
		])

		mean = np.array([mean_x, mean_y])

		dist = multivariate_normal(mean=mean, cov=Cov, allow_singular=True)

		def pdf(x):
			alpha = 0.7 # scale

			t, p = Torus.xyz_to_t_p(x[:,0], x[:,1], x[:,2])
			t_p = np.column_stack((t,p))

			# wrap until 3 * sigma_x
			k_t = int(np.ceil(3 * sigma_t / (2 * np.pi)))
			k_p = int(np.ceil(3 * sigma_p / (2 * np.pi)))

			total_pdf = np.zeros(t_p.shape[0])
			for i in range(-k_t, k_t+1):
				for j in range(-k_p, k_p+1):
					shifted_samples = np.column_stack((t_p[:,0] + i * 2 * np.pi, t_p[:,1] + j * 2 * np.pi))
					total_pdf += dist.pdf(shifted_samples)

			max = np.max(total_pdf)

			norm = total_pdf / max
			norm = norm * alpha
			return norm

		return pdf