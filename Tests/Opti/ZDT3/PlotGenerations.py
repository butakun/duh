from Backbone import *
import numpy as np
import matplotlib.pyplot as plt

CHAINFILENAME = "ZDT3.chain"
PLANFILENAME = "ZDT3.out.plan"
POPULATIONSIZE = 100

def ExtractNondominatedExps(pareto, plan):

	pop = ExperimentPlan(plan.Chain)
	pop.extend(plan)
	pop.extend(pareto)

	paretoNew = ExperimentPlan(plan.Chain)

	for i1 in xrange(len(pop)):
		exp1 = pop[i1]
		f1 = exp1.ResponsesAsVector()
		dominated = False
		for i2 in xrange(len(pop)):
			if i1 == i2:
				continue
			exp2 = pop[i2]
			f2 = exp2.ResponsesAsVector()
			if np.all(f1 > f2):	# only works if both objectives are to be minimized.
				dominated = True
				break
		if not dominated:
			paretoNew.append(exp1)

	return paretoNew

def Main():

	# load the chain and plan files.
	chain = Mothership.LoadChain(CHAINFILENAME)
	plan = ExperimentPlan(chain)
	plan.Import(open(PLANFILENAME))

	pareto = ExperimentPlan(chain)

	F = np.zeros((POPULATIONSIZE, 2)) # (POPULATIONSIZE x 2) matrix

	gen = 0
	while True:
		print "Generation ", gen
		pop = plan[gen * POPULATIONSIZE:(gen + 1) * POPULATIONSIZE]
		if len(pop) == 0:
			break
		pareto = ExtractNondominatedExps(pareto, pop)

		for i, exp in enumerate(pop):
			F[i, :] = exp.ResponsesAsVector()
		plt.plot(F[:, 0], F[:, 1], "o", color = "black")

		FP = np.zeros((len(pareto), 2))
		for i, exp in enumerate(pareto):
			FP[i, :] = exp.ResponsesAsVector()
		plt.plot(FP[:, 0], FP[:, 1], "o", color = "red")

		plt.axis([0.0, 1.0, 0.0, 1.0])
		plt.savefig("Gen_%03d.png" % gen)
		plt.close()

		gen += 1

if __name__ == "__main__":
	Main()

