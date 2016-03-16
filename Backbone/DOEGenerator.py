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
# $Id: DOEGenerator.py 130 2013-10-29 01:15:50Z kato $

from ExperimentPlan import ExperimentPlan
from Experiment import Experiment
from LHS import LHS
import Mothership
import numpy as n
import random, os

def Main(chainFileName, doeType, sampleCount, planFile):

	chain = Mothership.LoadChain(chainFileName)

	plan = ExperimentPlan(chain)

	add_ref = True
	if os.path.isfile(planFile):
		plan.Import(open(planFile))
		add_ref = False

	if add_ref:
		# Add the reference point as Experiment 0.
		exp = Experiment(0, chain)
		plan.append(exp)
		sampleCount -= 1
		print "Added the reference sample as Experiment 0"

	# Generate sampleCount - 1 samples by a DOE method.
	if doeType == "LHS":
		normalized = LHS(sampleCount, len(chain.Parameters))
		print "Generated %d samples by LHS" % sampleCount
	else:
		raise ValueError

	for i in range(sampleCount):
		expID = plan.NextAvailableID()
		exp = Experiment(expID, chain)
		p = normalized[i]
		print p
		for j in range(len(chain.Parameters)):
			xi = p[j]
			vmin = chain.Parameters[j]["Min"]
			vmax = chain.Parameters[j]["Max"]
			v = (1.0 - xi) * vmin + xi * vmax
			exp.Parameters[j]["Value"] = v
		plan.append(exp)

	plan.Export(open(planFile, "w"))

if __name__ == "__main__":
	import sys
	chainFileName = sys.argv[1]
	doeType = sys.argv[2]
	sampleCount = int(sys.argv[3])
	planFile = sys.argv[4]
	Main(chainFileName, doeType, sampleCount, planFile)

