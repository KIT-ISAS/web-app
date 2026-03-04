import importlib
import inspect
import pkgutil


class DistributionLoader:
	"""
	Class for loading different probability distributions with a plugin pattern.

	modeled after: https://www.researchgate.net/figure/Class-diagram-for-the-Plugin-Pattern_fig6_221039844
	"""
	def __init__(self, type, type_package):
		self.distribution_type = type
		self.distribution_package = type_package
		self.distributions = {}

		self.load_distributions()


	def load_distributions(self):
		pkg = importlib.import_module(self.distribution_package)
		if not hasattr(pkg, "__path__"):
			raise ValueError(f"'{self.distribution_package}' is not a package (missing __path__).")
		
		for finder, name, ispkg in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__name__ + "."):
			if "benchmark" in name:
				continue
			try:
				module = importlib.import_module(name)
			except Exception as e:
				print(f"Could not import distribution module '{name}': {e}")
				continue

			for _, obj in inspect.getmembers(module, inspect.isclass):
				# skip abstract, parametered intervace and non-subclasses
				if obj is self.distribution_type:
					continue
				if not issubclass(obj, self.distribution_type):
					continue
				if inspect.isabstract(obj):
					continue

				self.distributions[obj().get_name()] = obj()

	def get_distributions(self):
		return self.distributions
