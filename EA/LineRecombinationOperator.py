# $Id: LineRecombinationOperator.py 12 2010-04-09 15:12:40Z kato $

from RecombinationOperator import RecombinationOperator
import numpy as n

class LineRecombinationOperator(RecombinationOperator):

	def __init__(self, e1):
		"""
		Given two parents
		"""

		assert(e1 > 0.0)
		self.e1 = e1

	def Combine(self, individuals):

		assert(len(individuals) == 2)
		v1 = individuals[0].DesignParameters.AsVector()
		v2 = individuals[1].DesignParameters.AsVector()
		r = n.random.random()
		a = (1.0 - r) * (-self.e1) + r * (1.0 + self.e1)
		v = (1.0 - a) * v1 + a * v2

		offspring = individuals[0].Clone()
		offspring.Initialize()
		offspring.DesignParameters.SetToVector(v)
		return offspring

