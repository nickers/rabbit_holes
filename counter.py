from zope.interface import interface

class Counter(interface):
	def __init__(self):
		self.value = 0

	def increment(self):
		self.value += 1

	def getValue(self):
		return self.value

	def __adapt__(self):
		return self
