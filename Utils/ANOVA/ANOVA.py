# $Id: ANOVA.py 127 2013-05-17 16:35:24Z kato $

from Backbone import *
import Surrogate
import pylab
import numpy as np
import pickle, os.path

def Compute(chainFileName, planFileName, N, M, expRange = None):

	chain = Mothership.LoadChain(chainFileName)
	plan = ExperimentPlan(chain)
	plan.Import(open(planFileName))

	if expRange != None:
		expBegin, expEnd = expRange
		plan2 = ExperimentPlan(chain)
		for exp in plan:
			if expBegin <= exp.ID and exp.ID <= expEnd:
				plan2.append(exp)
		plan = plan2

	numParameters = len(chain.Parameters)
	numResponses = len(chain.Responses)
	numResponses2 = numResponses # # of responses to process

	pmin = np.array([ param["Min"] for param in chain.Parameters ])
	pmax = np.array([ param["Max"] for param in chain.Parameters ])
	print "pmin = ", pmin
	print "pmax = ", pmax

	db, ids = Surrogate.Utils.ResponseDatabaseFromPlan(plan, return_ids = True)

	model = Surrogate.RBFNetwork()
	model.Train(db)

	XX = LHS(N, numParameters)
	for i in range(N):
		XX[i, :] = (1.0 - XX[i, :]) * pmin + XX[i, :] * pmax

	# Total variance
	FF = np.zeros([N, numResponses])
	for i in range(N):
		X = XX[i, :]
		FF[i, :] = model.Evaluate(X)

	F0 = np.mean(FF[:, :], axis = 0)[:numResponses2]
	D = np.var(FF[:, :], axis = 0)[:numResponses2]
	print "F0 = ", F0
	print "D = ", D

	print "Responses"
	for i in range(numResponses2):
		print chain.Responses[i]["Name"]

	DDi = np.zeros([numParameters, numResponses2])
	S = np.zeros([numParameters + 1, numResponses2])
	Vi = np.zeros([numParameters, numResponses2])
	xx = np.zeros([N, numParameters])
	for i in range(numParameters):
		xxi = np.linspace(0.0, 1.0, M)
		#xxi = (1.0 - xxi) * pmin[i] + xxi * pmax[i]
		Fi = np.zeros([M, numResponses2])
		FFij = np.zeros([N, numResponses2])
		print "evaluating E(y|x%d)" % i
		for j in range(M):
			xi = xxi[j]
			xxj = LHS(N, numParameters - 1)
			xx[:, i] = xi
			if i > 0:
				xx[:, :i] = xxj[:, :i]
			if i < numParameters - 1:
				xx[:, i + 1:] = xxj[:, i:]
			for l in range(N):
				x = (1.0 - xx[l, :]) * pmin + xx[l, :] * pmax
				y = model.Evaluate(x)[:numResponses2]
				FFij[l, :] = y #model.Evaluate(xx[l, :])
			#Fi[j, :] = np.mean(FFij, axis = 0) - F0
			Fi[j, :] = np.mean(FFij, axis = 0)
			#print j, Fi[j, :]
		Di = np.var(Fi, axis = 0)
		DDi[i, :] = Di
		S[i, :] = Di / D
		#print "D%d = %f, D%d / D = %f" % (i, Di, i, Di / D)
		print "Parameter %d %s" % (i, chain.Parameters[i]["Name"])
		print S[i, :]

	print "Higher order index = "
	S[-1,:] = np.ones([numResponses2]) - (DDi.sum(axis = 0) / D)
	print S[-1, :]

	f = open("sobol.csv", "w")
	print >>f, ',', reduce(lambda a, b: a + ',' + b, [r["Name"] for r in chain.Responses])
	for i in range(numParameters):
		print >>f, "%s," % chain.Parameters[i]["Name"], reduce(lambda a, b: a + "," + b, map(lambda a: "%20.12e" % a, S[i, :]))
	print >>f, "Higher order,", reduce(lambda a, b: a + "," + b, map(lambda a: "%20.12e" % a, S[-1, :]))
	f.close()

def Post(looFileName):

	pass

def Synopsis():

	print "To compute Sobol indices (ANOVA)"
	print "  Swan ANOVA ChainFileName PlanFileName"
	print "    (Result will be saved as PlanFileName.sobol)"
	print "To view result:"
	print "  Swan ANOVA VIEW SobolFileName"

def Main(argv):

	if len(argv) < 3:
		Synopsis()
	elif argv[1] == "VIEW":
		Post(argv[2])
	else:
		N, M = 1000, 100
		if len(argv) >= 5:
			N, M = map(int, argv[3:5])
		Compute(argv[1], argv[2], N, M)

if __name__ == "__main__":

	import sys
	Main(sys.argv)

