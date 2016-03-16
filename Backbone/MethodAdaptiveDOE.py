# $Id: MethodAdaptiveDOE.py 136 2014-07-30 01:27:08Z kato $

from Method import Method
from Looper import Looper
from ExperimentPlan import ExperimentPlan
from Experiment import Experiment
from InfillSandbox import InfillSandbox
import AdaptiveDOECriteria
import Context
import threading, time

class MethodAdaptiveDOE(Method):

	def __init__(self, spec):
		Method.__init__(self)
		plan = ExperimentPlan(Context.SimulationChain)
		print "MethodDOE: ", spec
		plan.Import(open(spec["Plan"]))
		self.Plan = plan

		if spec.has_key("InfillCriteriaFunction"):
			self.InfillCriteriaFunction = spec["InfillCriteriaFunction"]
		else:
			self.InfillCriteriaFunction = AdaptiveDOECriteria.SimpleLOO
		self.MaxIterations = spec["Iterations"]
		self.NewSitesPerIteration = spec["NewSitesPerIteration"]

		self._Sem = threading.Semaphore(0)

	def Start(self):

		for iteration in range(self.MaxIterations):

			print "Adaptive DOE, Iteration %d" % (iteration + 1)
			self.ChooseNewSites(self.NewSitesPerIteration)

			for exp in self.Plan:
				if exp.Status == "READY":
					Context.Launcher.PostExperiment(exp, [self.ExperimentDone, exp])

			while True:
				print "*** MethodDOE acquiring semaphore"
				flag = self._Sem.acquire()
				print "*** MethodDOE acquired semaphore"
				assert(flag)

				self.Lock()
				exit = False
				if all(map(lambda e: e.IsDoneOrError(), self.Plan)):
					exit = True
				self.Unlock()
				if exit:
					break

		filename = "DOE.%s.out.plan" % Context.Name
		print "*** MethodDOE: exiting"
		print "*** MethodDOE: saving the experiment plan to %s" % filename
		self.Plan.Export(open(filename, "w"))

	def ExperimentDone(self, exp):
		filename = "DOE.%s.tmp.plan" % Context.Name
		print "*** MethodDOE Experiment %d done!, saving %s" % (exp.ID, filename)
		self.Plan.Export(open(filename, "w"))
		print "*** MethodDOE releasing semaphore"
		self._Sem.release()
		print "*** MethodDOE released semaphore"

	def ChooseNewSites(self, numNewSites):

		plan2 = ExperimentPlan(Context.SimulationChain)
		for exp in self.Plan:
			if exp.IsSuccess():
				plan2.append(exp)

		self.InfillCriteriaFunction(self.Plan)

		sandbox = InfillSandbox(Context.SimulationChain)

		for exp in plan2:
			err = exp["Error"]
			sandbox.AddSite(exp.ParametersAsVector(), err)

		newSites = sandbox.FindNewSites(numNewSites)

		xmin, xmax, xref = Context.SimulationChain.ParameterSpecsAsVectors()
		for i, site in enumerate(newSites):
			x, potential, nearest = site
			print "New Site %d: potential = %f" % (i, potential)
			print "  X = ", x
			print "  S = ", plan2[nearest].ParametersAsVector()
			print "  X(normalied) = ", (x - xmin) / (xmax - xmin)

		# Do not modify "plan" below this line
		for site in newSites:
			x, potential, nearest = site
			newID = self.Plan.NextAvailableID()
			e = Experiment(newID, Context.SimulationChain)
			e.SetParameters(x)
			self.Plan.append(e)

