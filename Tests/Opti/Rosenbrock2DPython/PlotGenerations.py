from Backbone import *
import numpy as np
import matplotlib.pyplot as plt

CHAINFILENAME = "Rosenbrock2D.chain"
PLANFILENAME = "Rosenbrock2D.out.plan"
POPULATIONSIZE = 200

def Main():

	# grid points for 2-D Rosenbrock contours
	Xc = np.arange(-2.0, 2.0, 0.04)
	Yc = np.arange(-2.0, 2.0, 0.04)
	Xc, Yc = np.meshgrid(Xc, Yc)
	Zc = (1.0 - Xc) * (1.0 - Xc) + 100.0 * (Yc - Xc * Xc) * (Yc - Xc * Xc)

	# load the chain and plan files.
	chain = Mothership.LoadChain(CHAINFILENAME)
	plan = ExperimentPlan(chain)
	plan.Import(open(PLANFILENAME))

	XY = np.zeros((POPULATIONSIZE, 2)) # (POPULATIONSIZE x 2) matrix

	for i, exp in enumerate(plan):
		ngeneration = i / POPULATIONSIZE
		ii = i % POPULATIONSIZE
		XY[ii, :] = exp.ParametersAsVector()
		if ii == POPULATIONSIZE - 1:
			plt.contour(Xc, Yc, Zc, 200)
			plt.plot(XY[:, 0], XY[:, 1], "o")
			plt.axis([-2.0, 2.0, -2.0, 2.0])
			plt.savefig("Gen_%03d.png" % ngeneration)
			plt.close()

if __name__ == "__main__":
	Main()

