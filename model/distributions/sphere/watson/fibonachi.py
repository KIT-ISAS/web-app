from abc import ABC, abstractmethod
import numpy as np
import scipy
import scipy.integrate
import scipy.interpolate
import sphstat
from pyrecest.backend import array
from pyrecest.distributions import WatsonDistribution as WatsonDistributionPyrecest
from scipy.special import erf, erfi, erfinv

from model.distributions.sphere.sphere_sampling_schema import SphereSamplingSchema
from util.selectors.silder_log import LogSlider
from model.sphere.sphere import Sphere
from util.selectors.silder_manual_input_wrapper import SliderManualInputWrapper as MI



class WatsonFibonachiSampling(SphereSamplingSchema):
	def __init__(self):
		self.sample_options = [
			MI(LogSlider("Number of Samples", 10, 100, 10000)),
		]
		
	def get_name(self):
		return "Fibonacci Lattice"


	def sample(self, sample_options, distribution_options):
		return self.sample_closed(sample_options, distribution_options)
		
	def sample_inverse_interpolation(self, sample_options, distribution_options):
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
			# 2pi comes from integrating over phi from 0 to 2pi
			# sin(theta): d S^2 = sin(theta) d theta d phi
			return 2* np.pi * pdf(0, t) * np.sin(t) # choose phi = 0 because of symmetry
		
		t_span = (0, np.pi) # theta from 0 to pi
		y0 = 0 # the value of the integrated pdf at 0 is 0

		sol = scipy.integrate.solve_ivp(f, t_span, [y0], rtol=1e-9, atol=1e-12)

		x = sol.t
		y = sol.y[0]

		
		# due to numerical issues, for large kappa and samplecount, y can be slightly non monotonic
		# monotonicity is needed for interpolation, so maximum.accumulate then bump by eps
		y = np.maximum.accumulate(y) 
		y /= y[-1] # normalize to [0,1]
		eps = 1e-14
		y += eps * np.arange(len(y)) 
	
		# now interpolate, but we swamp x and y so whe get the inverse function
		# this works because the function is monotonic
		# use PCHIP interpolation
		q = scipy.interpolate.PchipInterpolator(x=y, y=x)
		

		i = np.linspace(0, 1, sample_count, endpoint=False) + 0.5/sample_count # avoid poles by using centered kronecker lattice variant
		theta_i = q(i)
		w = np.cos(theta_i)

		indices = np.arange(0, sample_count)
		gold_seq = (1+5**0.5)/2  # golden ratio

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f

	# same as sample, but using inverse ODE to solve, simmilar to https://isas.iar.kit.edu/pdf/FUSION25_Frisch.pdf Sec. V.D
	# doesn't work for really big kappa due to numerical issues
	def sample_inverse_ode(self, sample_options, distribution_options):
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

		# compute this is the inverse of the f from the above sample() method
		def f(p,w):
			# w = cos(theta), because sin(theta) is 0 for 0 and pi => divide by 0
			w = np.clip(w, -1, 1)
			theta = np.arccos(w)
			return  1/ ( (2*np.pi) * pdf(0, theta)) # choose phi = 0 because of symmetry
		

		i = np.linspace(0, 1, sample_count)

		p_span = (0,1)
		y0 = -1


		# now compute the ode
		sol = scipy.integrate.solve_ivp(f, p_span, [y0], t_eval=i, dense_output=True, method="Radau")

		i = np.linspace(0, 1, sample_count, endpoint=False) + 0.5/sample_count
		w = sol.sol(i) # shape (1,n)
		w = np.squeeze(w)

		indices = np.arange(0, sample_count)
		gold_seq = (1+5**0.5)/2  # golden ratio

		w = np.clip(w, -1, 1) # needed due to floating point impresision
	
		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f
	
	@staticmethod
	def erfi_inv(y, iters=8, thresh=1.5):
		y = np.asarray(y, dtype=float)
		sgn = np.sign(y)
		z = np.abs(y)

		x = np.zeros_like(z)
		mask = z > 0
		if not np.any(mask):
			return x  # all zeros

		z_nz = z[mask]
		x0 = np.empty_like(z_nz)

		# Small region: Taylor
		small = z_nz <= thresh
		large = ~small

		x0[small] = z_nz[small] * np.sqrt(np.pi) / 2.0

		# Large region: leading asymptotic, ignoring 1/x
		if np.any(large):
			t = np.log(z_nz[large] * np.sqrt(np.pi))
			t = np.maximum(t, 0.0)
			x0[large] = np.sqrt(t)

		# Newton
		x_new = x0
		for _ in range(iters):
			fx = erfi(x_new) - z_nz
			dfx = 2.0 / np.sqrt(np.pi) * np.exp(x_new**2)
			x_new = x_new - fx / dfx

		x[mask] = x_new
		return sgn * x


	def sample_closed(self, sample_options, distribution_options):

		sample_count = sample_options[0].state
		k = distribution_options[0].state # kappa

		gold_seq = (1+5**0.5)/2  # golden ratio

		indices = np.arange(0, sample_count)

		
		if k > 0:
			w = 1 / (np.sqrt(k)) * self.erfi_inv( ((1-2*indices + sample_count)/ sample_count) * erfi(np.sqrt(k)) )
		elif k < 0:
			la = -k
			w = 1 / (np.sqrt(la)) * erfinv( ((2*indices +1 - sample_count)/ sample_count) * erf(np.sqrt(la)) )
		elif k == 0:
			w = ((2*indices +1 - sample_count)/ sample_count)


		w = np.clip(w, -1.0, 1.0) # clamp to avoid sqrt warnings due to numerical issues

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0))

		return x_i_f
	

	def sample_events(self, sample_options, distribution_options):
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
			# 2pi comes from integrating over phi from 0 to 2pi
			# sin(theta): d S^2 = sin(theta) d theta d phi
			return 2* np.pi * pdf(0, t) * np.sin(t) # choose phi = 0 because of symmetry
		
		t_span = (0, np.pi) # theta from 0 to pi
		y0 = 0 # the value of the integrated pdf at 0 is 0


		# targets for events (centered variant, see above coment)
		i = np.linspace(0, 1, sample_count, endpoint=False) + 0.5/sample_count 
		events = []
		for target in i:
			def make_event(target):
				def event(t, y):
					return y[0] - target
				return event
			event = make_event(target)
			event.terminal = False
			event.direction = 1 # increasing
			events.append(event)


		sol = scipy.integrate.solve_ivp(f, t_span, [y0], events=events)
		try:
			event_thetas_i = np.array(sol.t_events).squeeze()
		except ValueError:
			# this sometimes happens for large samples counts, like kappa=-30 with 10k samples misses 2points
			# its probably fine to continue
			print("Warning: some points might have been missed")
			event_thetas_i = np.array([te[0] if te.size else np.nan for te in sol.t_events], float)
			event_thetas_i = event_thetas_i[~np.isnan(event_thetas_i)]

			sample_count = event_thetas_i.shape[0]

		w = np.cos(event_thetas_i)

		indices = np.arange(0, sample_count)
		gold_seq = (1+5**0.5)/2  # golden ratio

		x_i_f_0 = w
		x_i_f_1 = np.sqrt(1-w**2) * np.cos( (2 * np.pi * indices) / gold_seq)
		x_i_f_2 = np.sqrt(1-w**2) * np.sin( (2 * np.pi * indices) / gold_seq)
		x_i_f = np.column_stack((x_i_f_1, x_i_f_2, x_i_f_0)) # order so that mu=[0, 0, 1]
		return x_i_f
	
