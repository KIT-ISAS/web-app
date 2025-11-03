from abc import ABC, abstractmethod
import numpy as np
import scipy
import scipy.integrate
import scipy.interpolate
import sphstat
from pyrecest.backend import array
from pyrecest.distributions import WatsonDistribution as WatsonDistributionPyrecest

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider
from model.sphere.sphere import Sphere


class WatsonFibonachiSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			LogSlider("Number of Samples", 10, 100, 10000),
		]
		
	def get_name(self):
		return "Fibonacci Lattice"
	
	def sample(self, sample_options, distribution_options):
		kappa = distribution_options[0].state
		sample_count = sample_options[0].state
		
		mu = array([0.0, 0.0, 1.0])
		watson_dist = WatsonDistributionPyrecest(mu=mu, kappa=kappa)
		

		'''
			Note: the watson pdf is symetrical
			This means that it will always produce the same value for different
			azimuth angles (phi) at a given polar angle (theta).
		''' 
		def pdf(phi, theta):
			# polar angle: 0 ≤ θ ≤ π  (theta)
			# azimuth:     0 ≤ φ < 2π (phi)
			x, y, z = Sphere.spherical_to_cartesian(theta=theta, phi=phi)
			x = np.column_stack((x, y, z))
			wts = watson_dist.pdf(array(x))
			return wts

		def f(t,y):
			# ring at lattitude theta has radius 2pi * sin(theta)
			return (2*np.pi) * pdf(0, t) * np.sin(t) # choose phi = 0 because of symmetry
		
		t_span = (0, np.pi) # theta from 0 to pi
		y0 = 0 # the value of the integrated pdf at 0 is 0

		# now compute the ode
		sol = scipy.integrate.solve_ivp(f, t_span, [y0])

		x = sol.t
		y = sol.y[0]

		
		# due to numerical issues, for large kappa and samplecount, y can be slightly non monotonic
		# monotonicity is needed for interpolation, so maximum.accumulate then bump by eps

		y = np.maximum.accumulate(y) 	
		diffs = np.diff(y)
		mask = diffs <= 0
		if np.any(mask):
			eps = 1e-10
			y = y + eps * np.arange(len(x))
			y = np.maximum.accumulate(y)
	
		# now interpolate, but we swamp x and y so whe get the inverse function
		# this works because the function is monotonic
		# use PCHIP interpolation
		try:
			q = scipy.interpolate.PchipInterpolator(x=y, y=x)
		except Exception as e:
			print(y)
			print("----")
			print(x)
			raise e
		

		i = np.linspace(0, 1, sample_count)
		theta_i = q(i)
		w = np.cos(theta_i)

		indices = np.arange(0, sample_count)
		gold_seq = (1+5**0.5)/2  # golden ratio

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f