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

