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
# $Id: MethodOpti.py 135 2014-07-29 07:39:17Z kato $

from Method import Method
from ChainResponseEvaluator import ChainResponseEvaluator
import Factory, Context, EA, Surrogate
import numpy as np

class MethodOpti(Method):

	def __init__(self, spec):
		Method.__init__(self)

		self.Chromosome = Factory.Chromosome(Context.SimulationChain)
		self.ResEval = ChainResponseEvaluator()
		self.ResEval.Start()

		self.PenEval = Factory.CreatePenaltyEvaluator(spec)
		self.FitnessEval = EA.FitnessEvaluator()

		optiConfig = spec["OptimizerConfig"]
		popSize = optiConfig["PopulationSize"]
		self.OptimizerConfig = optiConfig

		postIterCallback = lambda gen, pop: self.PostIteration(gen, pop)

		self.BestExperiment = None

		if spec["Optimizer"] == "GA":
			self.Optimizer = EA.MonoObjectiveGA(self.Chromosome, self.ResEval, self.PenEval, self.FitnessEval, popSize, 2)
			self.Optimizer.PostIterationCallback = postIterCallback
			self.HistoryFile = open("%s.history.dat" % Context.Name, "w")
		elif spec["Optimizer"] == "SurrogateGA":
			Context.Database.Import(open(optiConfig["DOE"]))
			pop = Factory.PopulationFromPlan(self.Chromosome, Context.Database)
			self.Optimizer = EA.MonoObjectiveSurrogateGA(self.Chromosome, self.ResEval, self.PenEval, self.FitnessEval, pop)
		elif spec["Optimizer"] == "ParetoGA":
			self.Optimizer = EA.SPEA2(self.Chromosome, self.ResEval, self.PenEval, optiConfig["PopulationSize"], optiConfig["ArchiveSize"])
		elif spec["Optimizer"] == "ParetoSurrogateGA":
			Context.Database.Import(open(optiConfig["DOE"]))
			pop = Factory.PopulationFromPlan(self.Chromosome, Context.Database)
			self.Optimizer = EA.ParetoSurrogateGA(self.Chromosome, self.ResEval, self.PenEval, pop,
				popSize, optiConfig["ArchiveSize"], optiConfig["Update"], optiConfig["UpdateTruncation"])

	def Start(self):

		print "MethodOpti: starting optimizer"
		self.Optimizer.Start(self.OptimizerConfig["Generations"])
		print "MethodOpti: optimizer finished"

		Context.Database.Export(open("%s.out.plan" % Context.Name, "w"))

		self.ResEval.PostQuit()

	def PostIteration(self, gen, pop):

		bestID = pop[0].ID
		bestExp = Context.Database.FindByID(bestID)
		resp = bestExp.ResponsesAsVector()
		param = bestExp.ParametersAsVector()
		resp_param = np.concatenate((resp, param))
		print >>self.HistoryFile, gen, "\t", reduce(lambda a, b: "%s\t%s" % (a, b), map(str, resp_param))

