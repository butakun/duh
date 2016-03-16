# $Id: DrunkRecombinationOperator.py 86 2011-02-17 16:46:06Z kato $

from RecombinationOperator import RecombinationOperator
from LineRecombinationOperator import LineRecombinationOperator
from BoxRecombinationOperator import BoxRecombinationOperator
import numpy as n

class DrunkRecombinationOperator(RecombinationOperator):

	def __init__(self):

		RecombinationOperator.__init__(self)
		ops = []
		ops.append(LineRecombinationOperator(0.25))
		ops.append(BoxRecombinationOperator(0.25))
		self.Operators = ops
		self.Wheel = [0.5, 1.0]

	def Combine(self, individuals):

		r = n.random.random()
		for i, op in enumerate(self.Operators):
			if r <= self.Wheel[i]:
				return op.Combine(individuals)
		raise ValueError
