import numpy as np

class Sphere:
	def __init__(self, resolution=50, radius=1):
		self.xyz = self.generate_xyz(resolution, radius)
		self.mesh = np.array([])
		self.samples = np.array([])

	def generate_xyz(self, resolution=50, radius=1):
		phi = np.linspace(0, np.pi, resolution)
		theta = np.linspace(0, 2 * np.pi, resolution)
		phi, theta = np.meshgrid(phi, theta)

		x = radius * np.sin(phi) * np.cos(theta)
		y = radius * np.sin(phi) * np.sin(theta)
		z = radius * np.cos(phi)

		return x, y, z