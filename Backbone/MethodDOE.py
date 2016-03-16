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
# $Id: MethodDOE.py 130 2013-10-29 01:15:50Z kato $

from Method import Method
from Looper import Looper
from ExperimentPlan import ExperimentPlan
from Experiment import Experiment
import Context
import threading, time

class MethodDOE(Method):

	def __init__(self, spec):
		Method.__init__(self)
		plan = ExperimentPlan(Context.SimulationChain)
		print "MethodDOE: ", spec
		plan.Import(open(spec["Plan"]))
		self.Plan = plan
		#self._Event = threading.Event()
		#self._Event.set()
		self._Sem = threading.Semaphore(0)

	def Start(self):

		for exp in self.Plan:
			if exp.Status == "READY":
				Context.Launcher.PostExperiment(exp, [self.ExperimentDone, exp])

		while True:
			flag = self._Sem.acquire()
			assert(flag)

			self.Lock()
			exit = False
			if all(map(lambda e: e.IsDoneOrError(), self.Plan)):
				exit = True
			self.Unlock()
			if exit:
				break

		print "*** MethodDOE: exiting"
		print "*** MethodDOE: saving the experiment plan to DOE_out.plan"
		self.Plan.Export(open("DOE.%s.out.plan" % Context.Name, "w"))

	def ExperimentDone(self, exp):
		print "*** MethodDOE Experiment %d done!" % exp.ID
		self.Plan.Export(open("DOE.%s.tmp.plan" % Context.Name, "w"))
		#self._Event.set()
		self._Sem.release()

