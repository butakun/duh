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
# $Id: MonoObjectiveSurrogateGA.py 132 2014-02-12 07:06:33Z kato $

from Population import *
from TournamentSelectionOperator import *
from DrunkRecombinationOperator import *
from SurrogateResponseEvaluator import *
from TrustRegion import *
from Value import *
from Penalty import *
from TorczonMeritFunction import *
import Surrogate
import copy, pickle

class MonoObjectiveSurrogateGA(object):

	def __init__(self, chromosome, resEval, penEval, fitnessEval, pop):

		self.Chromosome = chromosome
		self.ResEval = resEval
		self.PenEval = penEval
		self.FitnessEval = fitnessEval
		self.PopulationSize = 400
		self.Elitism = 2
		self.SelectionOp = TournamentSelectionOperator(2, 2)
		self.RecombinationOp = DrunkRecombinationOperator()
		self.MutationOp = None

		self.PenEval.Evaluate(pop)
		self.FitnessEval.Evaluate(pop)
		pop.SortByFitness()

		self.Population = pop
		rdb = Surrogate.ResponseDatabaseFromPopulation(self.Population)
		sdb = Surrogate.SuccessDatabaseFromPopulation(self.Population)
		self.ResponseModel = Surrogate.RBFNetwork()
		self.ResponseModel.Train(rdb)
		self.SuccessModel = Surrogate.RBFNetwork()
		self.SuccessModel.Train(sdb)
		self.SurrogateResEval = SurrogateResponseEvaluator(self.ResponseModel, self.SuccessModel, self.Chromosome)

		self.SurrogateChromosome = self.Chromosome.Clone()
		self.SurrogateChromosome.Responses.append(Value("TorczonMerit", "FLOAT", 0.0))
		self.SurrogatePenEval = copy.deepcopy(self.PenEval)
		self.SurrogatePenEval.ObjectivePenalties.append(Penalty("MAXIMIZE", "TorczonMerit", exponent = 1.0))
#		self.SurrogatePenEval.ConstraintPenalties.append(Penalty("LOWER_BOUND", "__SUCCESS__", 100.0, 1.0, 0.5))

		self.TrustRegion = TrustRegion(self.SurrogateChromosome)
		self.TrustRegionSize = 1.0
		self.TrustRegionCoeffWhenImproved = 1.3 # 1.2
		self.TrustRegionCoeffWhenNotImproved = 0.9 # 0.7
		self.TrustRegionSizeMinimum = 0.05

		self.MeritWeight = 0.01

		self.HistoryOutput = open("history.dat", "w")

	def Start(self, maxIter = 50):

		torczon = TorczonMeritFunction(self.Population, self.Chromosome, self.MeritWeight, "TorczonMerit")
		torczonFreq = 4
		notimproved = 0
		freezing = 10

		for idesign in range(maxIter):

			#self.DumpState(open("I%04d.pickle" % idesign, "w"))

			# Torczon Merit Weight Cycling
			if idesign % torczonFreq == 0:
				weight = self.MeritWeight
			elif idesign % torczonFreq == 1:
				weight = 0.1 * self.MeritWeight
			elif idesign % torczonFreq == 2:
				weight = 0.01 * self.MeritWeight
			elif idesign % torczonFreq == 3:
				weight = 0.001 * self.MeritWeight
			torczon.Weight = weight

			# Initialize the population used by surrogate-assisted GA
			pop = Population()
			for i in range(self.PopulationSize):
				#indi = self.SurrogateChromosome.Clone()
				indi = self.TrustRegion.Region.Clone()
				pop.append(indi)
			pop.Randomize()

			self.SurrogateResEval.Evaluate(pop)
			torczon.Evaluate(pop)
			self.SurrogatePenEval.Evaluate(pop)
			self.FitnessEval.Evaluate(pop)
			pop.SortByFitness()
			#print "Initial surrogate population =\n", pop

			# Surrogate iteration
			print "Surrogate-assisted GA campaign started"
			for j in range(50):
				newPop = Population()
				newPop.extend(pop[:self.Elitism])
				for i in range(self.Elitism, len(pop)):
					selected = self.SelectionOp.Select(pop)
					offspring = self.RecombinationOp.Combine(selected)
					# FIXME: mutation?
					#self.MutationOp.Mutate(offspring)
					offspring.ClipWithinBounds()
					newPop.append(offspring)
				pop = newPop
				self.SurrogateResEval.Evaluate(pop)
				torczon.Evaluate(pop)
				self.SurrogatePenEval.Evaluate(pop)
				self.FitnessEval.Evaluate(pop)
				pop.SortByFitness()
				#print pop[0]

			#print "Final population =\n", pop
			print "Best candidate (estimate by surrogate) =\n", pop[0]

			# Evaluate the optimum candidate
			candidates = Population()
			indi = self.Chromosome.Clone()
			indi.DesignParameters.SetToVector(pop[0].DesignParameters.AsVector())
			candidates.append(indi)
			print "Optimum candidates =\n", candidates
			self.ResEval.Evaluate(candidates)
			self.PenEval.Evaluate(candidates)
			self.FitnessEval.Evaluate(candidates)
			print "Optimum candidates (corrected) =\n", candidates

			candidates.SortByFitness()
			bestCandidate = candidates[0]
			bestSoFar = self.Population[0]
			print "Best candidate =\n", bestCandidate
			print "Best so far =\n", bestSoFar
			print "Trust region:\n", self.TrustRegion
			self.DumpHistory(idesign, bestSoFar)
			improved = bestCandidate.Fitness > bestSoFar.Fitness
			if improved:
				print "IMPROVED"
				self.TrustRegionSize *= self.TrustRegionCoeffWhenImproved
				self.TrustRegionSize = min(1.0, self.TrustRegionSize)
				center = bestCandidate.DesignParameters.AsVector()
				notimproved = 0
			else:
				print "DID NOT IMPROVE"
				notimproved += 1
				if notimproved > 5:
					print "Did not improved in the last 5 iterations, resetting the trust region."
					self.TrustRegionSize = 1.0
					center = None
					notimproved = 0
				else:
					self.TrustRegionSize *= self.TrustRegionCoeffWhenNotImproved
					center = bestCandidate.DesignParameters.AsVector()
					#center = bestSoFar.DesignParameters.AsVector()
			self.TrustRegionSize = max(self.TrustRegionSizeMinimum, self.TrustRegionSize)
			if idesign < freezing:
				# Don't tamper with the trust region at first
				self.TrustRegionSize = 1.0
				self.TrustRegion.Reset()
			else:
				self.TrustRegion.Resize(self.TrustRegionSize, center)

			self.Population.extend(candidates)
			self.Population.SortByFitness()

			# Extract samples to use for the next design iteration
			for i in range(50):
				trainingPop = self.TrustRegion.FilterPopulation(self.Population)
				if len(trainingPop) >= min(len(self.Chromosome.DesignParameters), len(filter(lambda i: i.Success, self.Population))):
					break
				print "Not enough samples in the trust region, so I'm enlarging it"
				self.TrustRegionSize *= 1.1
				self.TrustRegionSize = min(1.0, self.TrustRegionSize)
				self.TrustRegion.Resize(self.TrustRegionSize)
			print "Trust region: size coefficient = %f\n" % self.TrustRegionSize, self.TrustRegion

			torczon = TorczonMeritFunction(self.Population, self.Chromosome, self.MeritWeight, "TorczonMerit")

			# Re-train the surrogate model
			rdb = Surrogate.ResponseDatabaseFromPopulation(trainingPop)
			self.SurrogateResEval.ResponseSurrogate.Train(rdb)
			sdb = Surrogate.SuccessDatabaseFromPopulation(trainingPop)
			self.SurrogateResEval.SuccessSurrogate.Train(sdb)
			print "Surrogate models updated and re-trained with dbs (response db %d, success db %d)" % (len(rdb), len(sdb))

	def DumpHistory(self, i, best):

			f = best.Responses.AsVector()
			print >>self.HistoryOutput, i, "".join(["%20.12e" % n for n in f])

	def DumpState(self, o):

			a = {}
			a["ResponseSurrogate"] = self.SurrogateResEval.ResponseSurrogate
			a["SuccessSurrogate"] = self.SurrogateResEval.SuccessSurrogate
			a["TrustRegion"] = self.TrustRegion
			pickle.dump(a, o)

