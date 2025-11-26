from abc import ABC, abstractmethod

class Selector(ABC):
	def __init__(self):
		# this is the id of the last time the to_dash_component method was called
		# to_dash_component must have been called at least once for this to be set
		self.id = None

	# has the sideeffect of updating self.id
	@abstractmethod
	def to_dash_component(self, _type, id, renderer_id):
		pass

	def transfrom_down(x):
		# identity by default, override in subclasses if needed
		# does need to be defined if dash slider_values do not correspond to self.state
		return x
	
	def transfrom_up(x):
		# identity by default, override in subclasses if needed
		# does need to be defined if dash slider_values do not correspond to self.state
		return x

	def is_valid(x):
		# by default all values are valid
		# override in subclasses if needed
		return True
