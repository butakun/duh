# $Id: SOMTrain.py 66 2010-12-24 07:28:53Z kato $

from SOM import SOM
from CartesianGrid import CartesianGrid
from HexagonalGrid import HexagonalGrid
from Backbone import *
import SOMUtils
import numpy as n
import math as m

def TestSamples():

	samples = [
		[1, [10.0, 0.0, 0.0]],
		[2, [0.0, 1.0, 0.0]],
		[3, [0.0, 0.0, 1.0]],
		[4, [10.0, 1.0, 0.0]],
		[5, [0.0, 1.0, 1.0]],
		[6, [10.0, 0.0, 1.0]]
		]

	names = ["Red", "Green", "Blue"]

	return samples, names

def ComputeScales(samples):

	numSamples = len(samples)
	dims = len(samples[0][1])
	D = n.zeros((numSamples, dims))
	for i in range(numSamples):
		D[i, :] = samples[i][1]

	scales = n.ones(dims)
	mins = n.zeros(dims)
	for i in range(dims):
		vmin = n.min(D[:, i])
		vmax = n.max(D[:, i])
		mins[i] = vmin
		if vmax <= vmin:
			scales[i] = 1.0
		else:
			scales[i] = vmax - vmin

	return scales, mins

def Main(plan, names, sigma, sigmaDecay, alphaDecay):

	#samples, names = TestSamples()
	samples = SOMUtils.ExtractSOMSamples(plan, names)
	print "%d samples extracted" % len(samples), names

	scales, mins = ComputeScales(samples)
	dims = len(samples[0][1])

	# Neighborhood distance function.
	distFunc = lambda dsq: m.exp(-0.5 * dsq / (sigma * sigma))
	#som = SOM(CartesianGrid((20, 20)), dims, scales, distFunc)
	som = SOM(HexagonalGrid((20, 20)), dims, scales, distFunc)

	# Train the SOM.
	alpha = 1.0
	for i in range(100):
		if (i + 1) % 10 == 0:
			print "Iteration ", i + 1, "alpha = ", alpha, "sigma = ", sigma
		for id, sample in samples:
			som.Train(sample, alpha)
		alpha = alpha * alphaDecay
		sigma = sigma * sigmaDecay
		som.DistFunc = lambda dsq: m.exp(-0.5 * dsq / (sigma * sigma))

	SOMUtils.ExportSOM(open("OUT.som", "w"), som, names, samples)

if __name__ == "__main__":

	import sys

	if len(sys.argv) < 6:
		print "%s ChainFile PlanFile Sigma SigmaDecay AlphaDecay VarName1 VarName2 ..." % sys.argv[0]
	else:
		chain = Mothership.LoadChain(sys.argv[1])
		plan = ExperimentPlan(chain)
		plan.Import(open(sys.argv[2]))
		sigma = float(sys.argv[3])
		sigmaDecay = float(sys.argv[4])
		alphaDecay = float(sys.argv[5])
		Main(plan, sys.argv[6:], sigma, sigmaDecay, alphaDecay)

