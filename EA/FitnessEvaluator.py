#    duh, a heuristics-based design exploration code.
#    Copyright (C) 2016 Hiromasa Kato <hiromasa at gmail.com>
#
#    This file is part of duh.
#
#    duh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    duh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

