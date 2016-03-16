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
# $Id: ChainResponseEvaluator.py 135 2014-07-29 07:39:17Z kato $

from Looper import Looper
import Context, Factory
import threading

class ChainResponseEvaluator(Looper):

	def __init__(self):
		Looper.__init__(self)
		self.RLock = threading.RLock()
		self.AllDone = threading.Event()
		self.Individuals = None
		self.Exps = set() # set containing ExpIDs currently running, the evaluation of a population is done when this set is empty.

	def MessageReceived(self, msg):

		if msg["what"] == "EVALUATE":
			exp = msg["exp"]
			#print "ChainResEval: posting experiment %d" % exp.ID
			Context.Launcher.PostExperiment(exp, [self.ExperimentDone, exp])
		else:
			Looper.MessageReceived(self, msg)

	def ExperimentDone(self, exp):

		print "ChainResEval: Experiment %d has been completed, status = %s" % (exp.ID, exp.Status)
		allDone = False
		self.RLock.acquire()
		self.Exps.remove(exp.ID)
		#print "ChainResEval: Exps = ", self.Exps

		indi = self.Individuals.FindByID(exp.ID)
		self.FromExperimentToIndividual(exp, indi)

		allDone = len(self.Exps) == 0
		if allDone:
			self.AllDone.set()
		self.RLock.release()

	def Evaluate(self, pop):

		#print "ChainResEval: evaluating pop"

		assert(len(self.Exps) == 0)

		self.Individuals = pop
		nextID = Context.Database.NextAvailableID()

		exps = []
		for indi in pop:
			exp = Factory.ExperimentFromIndividual(Context.SimulationChain, indi)
			exp.ID = nextID
			indi.ID = nextID
			Context.Database.append(exp)
			exps.append(exp)
			self.Exps.add(exp.ID)
			nextID += 1

		for exp in exps:
			self.PostMessage({"what":"EVALUATE", "exp":exp})

		while not self.AllDone.is_set():
			#print "ChainResEval: waiting"
			self.AllDone.wait(1.0)
		#print "ChainResEval: waiting over"
		self.AllDone.clear()
		self.Individuals = None

		Context.Database.Export(open("%s.tmp.plan" % Context.Name, "w"))

	def FromExperimentToIndividual(self, exp, indi):

		for r in indi.Responses:
			r.Value = exp.Response(r.Name)["Value"]
		indi.Success = exp.IsSuccess()

