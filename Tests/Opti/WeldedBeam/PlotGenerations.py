from Backbone import *
import numpy as np
import matplotlib.pyplot as plt

CHAINFILENAME = "WeldedBeam.chain"
PLANFILENAME = "WeldedBeam.out.plan"
POPULATIONSIZE = 200

def Main():

	# load the chain and plan files.
	chain = Mothership.LoadChain(CHAINFILENAME)
	plan = ExperimentPlan(chain)
	plan.Import(open(PLANFILENAME))

	HLTBs = np.zeros((POPULATIONSIZE, 4)) # (POPULATIONSIZE x 4) matrix

	for i, exp in enumerate(plan):
		ngeneration = i / POPULATIONSIZE
		ii = i % POPULATIONSIZE
		HLTBs[ii, :] = exp.ParametersAsVector()
		if ii == POPULATIONSIZE - 1:
			plt.figure(figsize = (20, 20))

			plt.subplot(331)
			plt.plot(HLTBs[:, 0], HLTBs[:, 1], "o") # h-l
			plt.axis([0.0, 2.0, 0.0, 10.0])
			plt.xlabel("h")
			plt.ylabel("l")

			plt.subplot(332)
			plt.plot(HLTBs[:, 0], HLTBs[:, 2], "o") # h-t
			plt.axis([0.0, 2.0, 0.0, 10.0])
			plt.xlabel("h")
			plt.ylabel("t")

			plt.subplot(333)
			plt.plot(HLTBs[:, 0], HLTBs[:, 3], "o") # h-b
			plt.axis([0.0, 2.0, 0.0, 2.0])
			plt.xlabel("h")
			plt.ylabel("b")

			plt.subplot(335)
			plt.plot(HLTBs[:, 1], HLTBs[:, 2], "o") # l-t
			plt.axis([0.0, 10.0, 0.0, 10.0])
			plt.xlabel("l")
			plt.ylabel("t")

			plt.subplot(336)
			plt.plot(HLTBs[:, 1], HLTBs[:, 3], "o") # l-b
			plt.axis([0.0, 10.0, 0.0, 2.0])
			plt.xlabel("l")
			plt.ylabel("b")

			plt.subplot(339)
			plt.plot(HLTBs[:, 2], HLTBs[:, 3], "o") # t-b
			plt.axis([0.0, 10.0, 0.0, 2.0])
			plt.xlabel("t")
			plt.ylabel("b")

			plt.savefig("Gen_%03d.png" % ngeneration)
			plt.close()

if __name__ == "__main__":
	Main()

