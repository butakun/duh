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
# $Id: SPEA2.py 131 2014-01-01 13:57:57Z kato $

from Population import *
from TournamentSelectionOperator import *
from DrunkRecombinationOperator import *
from Penalty import Penalty
from Dominance import Dominance
from Truncator import Truncator
import numpy as np

class SPEA2FitnessEvaluator(object):

	def __init__(self, dominanceEval):

		self.DominanceEval = dominanceEval

	def Evaluate(self, pop):

		N = len(pop)

		for indi in pop:
			indi.Fitness = 0.0

		for i1 in range(N):
			indi1 = pop[i1]
			# Strength assignment
			S = 0 # Strength of indi1
			dominated = [] # list of individuals dominated by indi1
			for i2 in range(N):
				if i1 == i2:
					continue
				indi2 = pop[i2]
				if self.DominanceEval.FirstDominatesSecond(indi1, indi2):
					S += 1
					dominated.append(indi2)
			# Raw fitness (Here, we negate the raw fitness as defined in the original paper, because we want fitness to be the bigger the better)
			for indi in dominated:
				indi.Fitness -= S

class SPEA2(object):

	def __init__(self, chromosome, resEval, penEval, popSize, archiveSize):

		self.Chromosome = chromosome
		self.ResEval = resEval
		self.PenEval = penEval
		self.FitnessEval = SPEA2FitnessEvaluator(Dominance())
		self.PopulationSize = popSize
		self.ArchiveSize = archiveSize

		self.SelectionOp = TournamentSelectionOperator(2, 2)
		self.RecombinationOp = DrunkRecombinationOperator()
		self.MutationOp = None
		self.Population = None
		self.Archive = None
		self.HistoricPopulation = None # records the entire population of the entire generation for later inspection
		self.HistoricArchive = None # records the entire archive of the entire generation for later inspection

		self.PenEval.ConstraintPenalties.append(Penalty("LOWER_BOUND", "__SUCCESS__", 1.0, 1.0, 0.5))

		self.Truncator = Truncator("OBJECTIVE")

	def Start(self, maxIter = 50):

		# Initialize
		self.Population = Population()
		for i in range(self.PopulationSize):
			indi = self.Chromosome.Clone()
			indi.Randomize()
			self.Population.append(indi)
		self.Archive = Population()

		self.ResEval.Evaluate(self.Population)
		self.PenEval.Evaluate(self.Population)

		self.HistoricPopulation = Population()
		self.HistoricPopulation.extend(self.Population)
		self.HistoricArchive = Population()
		self.HistoricArchive.extend(self.Archive)

		print "Generation 0"
		#print "Population"
		#print self.Population
		#print "Archive"
		#print self.Archive

		for gen in range(1, maxIter + 1):

			pop = Population()
			pop.extend(self.Population)
			pop.extend(self.Archive)
			self.FitnessEval.Evaluate(pop) # Assign raw fitness values

			# Extract nondominated individuals (i.e., raw fitness == 0)
			nondominated = pop.Filter(lambda i: i.Fitness == 0.0)

			# New archive
			archive = nondominated
			nn = len(archive)
			if nn > self.ArchiveSize:
				# Truncate
				archive = self.Truncator.Truncate(archive, self.ArchiveSize)
			elif nn < self.ArchiveSize:
				# Add dominated individuals to the archive
				dominated = pop.Filter(lambda i: i.Fitness < 0.0) # our raw fitness is the negative of the Zitzler's definition.
				dominated.SortByDecreasingFitness()
				for i in range(self.ArchiveSize - nn):
					archive.append(dominated[i])
			assert(len(archive) == self.ArchiveSize)

			# Select from the new archive
			newPop = Population()
			for i in range(self.PopulationSize):
				selected = self.SelectionOp.Select(archive)
				offspring = self.RecombinationOp.Combine(selected)
				#self.MutationOp.Mutate(offspring)
				offspring.ClipWithinBounds()
				newPop.append(offspring)

			self.Archive = archive
			self.Population = newPop
			self.ResEval.Evaluate(self.Population)
			self.PenEval.Evaluate(self.Population)

			print "Generation %d" % gen
			#print "Population"
			#print self.Population
			#print "Archive"
			#print self.Archive
			self.HistoricPopulation.extend(self.Population)
			self.HistoricArchive.extend(self.Archive)

def DumpObjectives(f, pop):

	for indi in pop:
		o = indi.Objectives
		print >>f, o[0], o[1]

def TestTruncation():

	M = 20
	N = 5
	f1 = np.random.random(M)
	f2 = np.array(f1)

	pop = Population()
	for i in range(M):
		indi = Individual()
		indi.Objectives = np.array([f1[i], f2[i]])
		pop.append(indi)

	DumpObjectives(open("0.dat", "w"), pop)

	truncated = Truncate(pop, N)
	DumpObjectives(open("1.dat", "w"), truncated)

if __name__ == "__main__":
	TestTruncation()

