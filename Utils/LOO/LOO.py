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
# $Id: LOO.py 131 2014-01-01 13:57:57Z kato $

from Backbone import *
import Surrogate
import pylab
import numpy as n
import pickle, os.path

def LeaveOneOutFromDB(db, iloo):

	assert(iloo < len(db))

	db2 = Surrogate.Database()
	for i in range(len(db)):
		if i == iloo:
			continue
		db2.append(db[i])
	return db2

def LeaveOneOut(plan):

	# Only successful experiments will be included in the database.
	db, ids = Surrogate.Utils.ResponseDatabaseFromPlan(plan, return_ids = True)

	X, F, FLOO = [], [], []
	for i in range(len(db)):
		x = db[i][0]
		f = db[i][1]
		dbLOO = LeaveOneOutFromDB(db, i)
		rbfn = Surrogate.RBFNetwork()
		rbfn.Train(dbLOO)
		fLOO = rbfn.Evaluate(x)
		X.append(x)
		F.append(f)
		FLOO.append(fLOO)
	F = n.array(F)
	FLOO = n.array(FLOO)

	return F, FLOO, ids

def Compute(chainFileName, planFileName, expRange = None):

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

	numResponses = len(chain.Responses)

	F, FLOO, ids = LeaveOneOut(plan)

	responseNames = map(lambda r: r["Name"], chain.Responses)

	stem = os.path.basename(planFileName).replace(".plan", "")
	pickle.dump([F, FLOO, responseNames], open("%s.loo" % stem, "w"))

	# Save the true vs. surrogate data points
	f = open(stem + ".loocsv", "w")
	numSamples = F.shape[0]
	for j in range(numResponses):
		print "Correlation Coefficient for Response %s" %  responseNames[j]
		r = n.corrcoef(F[:, j], FLOO[:, j])[0, 1]
		print "  r = ", r

		print >>f, "# Leave-One-Out for Response %s" % responseNames[j]
		print >>f, "R =\t%f" % r
		print >>f, responseNames[j], '\t', "%s (surrogate)" % responseNames[j]
		for i in range(numSamples):
			print >>f, F[i, j], '\t', FLOO[i, j], "\t# Exp %d" % ids[i]
		print >>f, "# Line of Perfect Fit"
		Fmin = n.min(F[:, j])
		Fmax = n.max(F[:, j])
		print >>f, "%e\t%e" % (Fmin, Fmin)
		print >>f, "%e\t%e" % (Fmax, Fmax)
	f.close()

	# ...
	dF = n.abs(F - FLOO)
	ei = []
	for i in range(numResponses):
		ei.append(dF[:, i].argsort())

def Post(looFileName):

	F, FLOO, responseNames = pickle.load(open(looFileName))
	numResponses = F.shape[1]

	for j in range(numResponses):
		print "Correlation Coefficient for Response %s" %  responseNames[j]
		r = n.corrcoef(F[:, j], FLOO[:, j])[0, 1]
		print "  r = ", r
		pylab.figure()
		pylab.plot(F[:, j], FLOO[:, j], "o")
		Fmin = n.min(F[:, j])
		Fmax = n.max(F[:, j])
		pylab.title(responseNames[j])
		pylab.plot([Fmin, Fmax], [Fmin, Fmax])
	pylab.show()

def Synopsis():

	print "To compute Leave-One-Out Cross-Validation:"
	print "  Swan LOO ChainFileName PlanFileName"
	print "    (Result will be saved as PlanFileName.loo)"
	print "To view result:"
	print "  Swan LOO VIEW LooFileName"

def Main(argv):

	if len(argv) < 3:
		Synopsis()
	elif argv[1] == "VIEW":
		Post(argv[2])
	else:
		if len(argv) >= 5:
			expBegin = int(argv[3])
			expEnd   = int(argv[4])
			Compute(argv[1], argv[2], [expBegin, expEnd])
		else:
			Compute(argv[1], argv[2])

if __name__ == "__main__":

	import sys
	Main(sys.argv)

