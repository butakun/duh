# $Id: PenaltyEvaluator.py 2 2010-02-26 14:01:03Z kato $

from PopulationEvaluator import PopulationEvaluator
from Penalty import Penalty
import numpy as n

class PenaltyEvaluator(PopulationEvaluator):

	def __init__(self):

		self.ObjectivePenalties = []
		self.ConstraintPenalties = []

	def Function(self, indi):

		o, c = [], []
		for penalty in self.ObjectivePenalties:
			o.append(penalty.Apply(indi))
		for penalty in self.ConstraintPenalties:
			c.append(penalty.Apply(indi))
		o = n.array(o)
		c = n.array(c)

		indi.Objectives = o
		indi.Constraints = c

