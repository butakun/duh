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
# $Id: MonoObjectiveGA.py 135 2014-07-29 07:39:17Z kato $

from Optimizer import Optimizer
from Population import *
from TournamentSelectionOperator import *
from DrunkRecombinationOperator import *
from Penalty import Penalty

class MonoObjectiveGA(Optimizer):

	def __init__(self, chromosome, resEval, penEval, fitnessEval, popSize, elitism):

		Optimizer.__init__(self)

		self.Chromosome = chromosome
		self.ResEval = resEval
		self.PenEval = penEval
		self.FitnessEval = fitnessEval
		self.PopulationSize = popSize
		self.Elitism = elitism
		self.SelectionOp = TournamentSelectionOperator(2, 2)
		self.RecombinationOp = DrunkRecombinationOperator()
		self.MutationOp = None
		self.Population = None

		self.PenEval.ConstraintPenalties.append(Penalty("LOWER_BOUND", "__SUCCESS__", 1.0, 1.0, 0.5))

	def Start(self, maxIter = 50):

		self.Population = Population()
		for i in range(self.PopulationSize):
			indi = self.Chromosome.Clone()
			indi.Randomize()
			self.Population.append(indi)

		self.ResEval.Evaluate(self.Population)
		self.PenEval.Evaluate(self.Population)
		self.FitnessEval.Evaluate(self.Population)
		self.Population.SortByFitness()

		for gen in range(maxIter):
			newPop = Population()
			newPop.extend(self.Population[:self.Elitism])
			for i in range(self.Elitism, len(self.Population)):
				selected = self.SelectionOp.Select(self.Population)
				offspring = self.RecombinationOp.Combine(selected)
				# FIXME: mutation?
				#self.MutationOp.Mutate(offspring)
				offspring.ClipWithinBounds()
				newPop.append(offspring)
			self.Population = newPop
			self.ResEval.Evaluate(self.Population)
			self.PenEval.Evaluate(self.Population)
			self.FitnessEval.Evaluate(self.Population)
			self.Population.SortByFitness()
			print "Generation %d" % (gen + 1)
			print self.Population[0]
			if self.PostIterationCallback != None:
				self.PostIterationCallback(gen, self.Population)

