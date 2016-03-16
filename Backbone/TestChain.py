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
# $Id: TestChain.py 44 2010-09-21 15:31:56Z kato $

import Context, Mothership
from MultiLevelChain import MultiLevelChain
from Experiment import Experiment
from ExperimentPlan import ExperimentPlan
import os, shutil, time, threading

DONE = None

def Done(exp):

	DONE.set()

def Main():

	open("Parameters.in.template", "w").write("""TEST
X1	=	1.0
X2	=	1.2
""")

	spec = {}
	execfile("Opti.chain", globals(), spec)

	assert(spec["Type"] == "MultiLevel")

	chain = MultiLevelChain(spec)

	Mothership.Initialize(chain)

	print "CHAIN PROPS"
	print chain.Parameters
	print chain.Responses
	print chain.SuccessFlags

	print "NEW EXPERIMENT"
	exp = Experiment(1, chain)
	print exp.Parameters
	print exp.Responses
	print exp.SuccessFlags

	global DONE
	DONE = threading.Event()
	Mothership.QueueExperiment(exp, [Done, exp])

	DONE.wait()

	print exp.Responses
	print exp.SuccessFlags
	print exp.Context
	print exp.Status

	plan = ExperimentPlan(chain)
	plan.append(exp)
	plan.Export(open("test.plan", "w"))

	Mothership.Finalize()

if __name__ == "__main__":
	Main()
	print "done"

