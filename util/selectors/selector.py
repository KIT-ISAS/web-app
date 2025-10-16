from abc import ABC, abstractmethod

class Selector(ABC):
	def __init__(self):
		# this is the id of the last time the to_dash_component method was called
		# to_dash_component must have been called at least once for this to be set
		self.id = None

	# has the sideeffect of updating self.id
	@abstractmethod
	def to_dash_component(self, id):
		pass