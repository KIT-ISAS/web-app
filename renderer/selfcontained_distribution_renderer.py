from model.selfcontained_distribution import SelfContainedDistribution

class SelfContainedDistributionRenderer:
	def __init__(self, distribution: SelfContainedDistribution):
		self.distribution = distribution

		self.plot_layout = distribution.plot_layout
		self.settings_layout = distribution.settings_layout

	def get_layout_components(self):
		return (self.settings_layout, self.plot_layout)