
"""
This is a class of distributions that do not utelize the dynamic distribution loading system,
and provide all their callbacks and data internally.

Meant to be used for simple distributions, where using the distribution loading system would be overkill.
To be used with the selfcontained_distribution_renderer.
"""
class SelfContainedDistribution:
	def __init__(self):
		self.settings_layout = [] # to be set by subclass
		self.plot_layout = [] # to be set by subclass