from abc import ABC, abstractmethod

class Selector(ABC):
	@abstractmethod
	def to_dash_component(self, id):
		pass