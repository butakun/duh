# $Id: Individual.py 84 2011-02-08 02:25:48Z kato $

from Values import Values
import copy
import numpy as n

class Individual(object):

	def __init__(self):

		self.ID = None
		self.DesignParameters = Values()
		self.Responses = Values()
		self.Success = False

		self.Objectives = None
		self.Constraints = None
		self.Fitness = None

	def Clone(self):
		"""
		Clones self, but the clone has no ID, i.e. ID == None
		"""

		indi = copy.deepcopy(self)
		indi.ID = None
		indi.Objectives = None
		indi.Constraints = None
		indi.Fitness = None
		return indi

	def Initialize(self):

		self.DesignParameters.Initialize()
		self.Responses.Initialize()
		self.ID = None
		self.Objectives = None
		self.Constraints = None
		self.Fitness = None

	def Randomize(self):

		for v in self.DesignParameters:
			v.Randomize()
		self.Success = False

	def ClipWithinBounds(self):

		for v in self.DesignParameters:
			v.Value = min(v.Value, v.MaxValue)
			v.Value = max(v.Value, v.MinValue)

	def ParameterSpaceDistanceTo(self, indi2):

		x1 = self.DesignParameters.AsVector()
		x2 = indi2.DesignParameters.AsVector()
		d = x2 - x1
		return n.sqrt(n.dot(d, d))

	def IsFeasible(self):

		if not self.Success:
			return False

		if self.Constraints == None:
			return True

		return self.Constraints.sum() == 0.0

	def __str__(self):

		return str(self.DesignParameters) + str(self.Responses) + str(self.Objectives) + str(self.Constraints) + " " + str(self.Success) + " " + str(self.Fitness)

