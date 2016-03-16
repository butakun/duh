# $Id: BoundedValue.py 11 2010-04-08 14:50:05Z kato $

from Value import Value
import random

class BoundedValue(Value):

	def __init__(self, name, valueType, value, refValue, minValue, maxValue):

		Value.__init__(self, name, valueType, value, refValue)
		self.MinValue = minValue
		self.MaxValue = maxValue
		assert(self.MinValue < self.MaxValue)
		assert(self.MinValue <= self.RefValue and self.RefValue <= self.MaxValue)

	def ClipWithinBounds(self):

		self.Value = min(self.MaxValue, max(self.Value, self.MinValue))

	def Randomize(self):

		r = random.random()
		self.Value = (1.0 - r) * self.MinValue + r * self.MaxValue

