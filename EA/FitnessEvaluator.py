# $Id: FitnessEvaluator.py 98 2011-08-19 03:11:13Z kato $

import numpy as n

class FitnessEvaluator(object):

	""" Deb's Constraint Fitness Evalator """

	def Evaluate(self, pop):

		# Initialize the worst feasible fitness, can be anything as long as it's actually from an individual.
		worstFeasibleFitness = -pop[0].Objectives.sum()

		feasibles = []
		nonfeasibles = []
		for indi in pop:
			if indi.IsFeasible():
				indi.Fitness = -indi.Objectives.sum()
				worstFeasibleFitness = min(worstFeasibleFitness, indi.Fitness)
				feasibles.append(indi)
			else:
				nonfeasibles.append(indi)
		#print "worst feasible fitness = ", worstFeasibleFitness

		if len(feasibles) == 0:
			worstFeasibleFitness = 0.0
		worstNonfeasibleFitness = worstFeasibleFitness

		failed = []
		for indi in nonfeasibles:
			if indi.Success:
				indi.Fitness = worstFeasibleFitness - indi.Constraints.sum()
				worstNonfeasibleFitness = min(worstNonfeasibleFitness, indi.Fitness)
			else:
				failed.append(indi)
		#print "worst nonfeasible fitness = ", worstNonfeasibleFitness

		failedFitness = worstNonfeasibleFitness - abs(worstNonfeasibleFitness)
		for indi in failed:
			indi.Fitness = failedFitness

	"""
	def Evaluate(self, pop):

		for indi in pop:
			indi.Fitness = -(n.sum(indi.Objectives) + n.sum(indi.Constraints))
	"""

