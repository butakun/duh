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
# $Id: ParetoSurrogateGA.py 131 2014-01-01 13:57:57Z kato $

from Population import *
from TournamentSelectionOperator import *
from DrunkRecombinationOperator import *
from SurrogateResponseEvaluator import *
from Value import *
from Penalty import *
from Truncator import Truncator
from SPEA2 import SPEA2
import Surrogate
import copy, pickle

class ParetoSurrogateGA(object):

	def __init__(self, chromosome, resEval, penEval, doe, popSize = 100, archiveSize = 50, updateSampleCount = 3, updateTruncation = "OBJECTIVE"):

		self.Chromosome = chromosome
		self.ResEval = resEval
		self.PenEval = penEval
		self.PopulationSize = popSize
		self.ArchiveSize = archiveSize
		self.UpdateSampleCount = updateSampleCount
		self.UpdateTruncation = updateTruncation

		self.Population = doe
		rdb = Surrogate.ResponseDatabaseFromPopulation(self.Population)
		sdb = Surrogate.SuccessDatabaseFromPopulation(self.Population)
		self.ResponseModel = Surrogate.RBFNetwork()
		self.ResponseModel.Train(rdb)
		self.SuccessModel = Surrogate.RBFNetwork()
		self.SuccessModel.Train(sdb)
		self.SurrogateResEval = SurrogateResponseEvaluator(self.ResponseModel, self.SuccessModel, self.Chromosome)

	def Start(self, maxIter = 50):

		for idesign in range(maxIter):

			# Surrogate-assisted SPEA2
			moga = SPEA2(self.Chromosome, self.SurrogateResEval, self.PenEval, self.PopulationSize, self.ArchiveSize)
			moga.Start(50)

			# Record the SPEA history
			pickle.dump(moga.HistoricPopulation, open("spea2.pop.%04d.pickled" % idesign, "w"))
			pickle.dump(moga.HistoricArchive, open("spea2.arc.%04d.pickled" % idesign, "w"))

			# Pick a subset of the archived individuals and use them to update the surrogate model
			truncator = Truncator(self.UpdateTruncation)
			newSamples = truncator.Truncate(moga.Archive, self.UpdateSampleCount)
			print "Selected %d individuals (via truncation) to be evaluated and added to the training sample set" % self.UpdateSampleCount

			# Evaluate the selected individuals
			self.ResEval.Evaluate(newSamples)
			self.PenEval.Evaluate(newSamples)

			self.Population.extend(newSamples)

			# Re-train the surrogate model
			rdb = Surrogate.ResponseDatabaseFromPopulation(self.Population)
			self.SurrogateResEval.ResponseSurrogate.Train(rdb)
			sdb = Surrogate.SuccessDatabaseFromPopulation(self.Population)
			self.SurrogateResEval.SuccessSurrogate.Train(sdb)
			print "Surrogate models updated and re-trained with dbs (response db %d, success db %d)" % (len(rdb), len(sdb))

