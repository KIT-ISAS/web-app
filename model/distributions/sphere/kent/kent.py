from abc import ABC, abstractmethod
from model.distributions.sphere.sphere_distribution import SphereDistribution
from model.sphere.sphere import Sphere
from util.selectors.slider import Slider 
from util.selectors.slider_float import FloatSlider
import numpy as np

from model.distributions.sphere.kent.random import KentRandomSampling
from sphstat.descriptives import rotationmatrix_withaxis

class KentDistribution(SphereDistribution):
	def __init__(self):
		self.distribution_options = [
			Slider("κ (kappa)", 0.0, 10.0, 50.0),
			Slider("β (beta)", 0.0, 2.0, 25.0),
		]
		
		self.sampling_methods = [
			KentRandomSampling()
		]

	def get_name(self):
		return "Kent (5-parameter Fisher-Bingham - FB5)"

	def get_pdf(self, distribution_options):
		# we don't compute the normalization constant $c(\kappa, \beta)$ here
		# because the density fucntions are plotted not to scale anyway
		c = 1.0

		kappa = distribution_options[0].state
		beta = distribution_options[1].state
		beta = min(beta, kappa / 2)

		# hardcoded, same as in kent random sampling
		y3 = np.array([1, 0, 0]).reshape(3, 1)
		y2 = np.array([0, 1, 0]).reshape(3, 1)
		y1 = np.array([0, 0, 1]).reshape(3, 1)
		


		def pdf(x):
			#print(f"{y1.T.shape} * {x.T.shape}")
			kent = 1/c * np.exp(
				kappa * (y1.T @ x.T) +
				beta * ( (y2.T @ x.T)**2 - (y3.T @ x.T)**2 )
			)
			kent = kent.flatten()
			max = np.max(kent)
			norm = kent / max
			return norm
		return pdf
				