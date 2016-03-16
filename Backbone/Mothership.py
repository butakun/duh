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
# $Id: Mothership.py 130 2013-10-29 01:15:50Z kato $
# This is a singleton.

import Context
from MultiLevelChain import MultiLevelChain
from MultiThreadDispatcher import MultiThreadDispatcher
from MethodDOE import MethodDOE
from MethodAdaptiveDOE import MethodAdaptiveDOE
from MethodOpti import MethodOpti
from Looper import Looper
from ExperimentLauncher import ExperimentLauncher
from ExperimentPlan import ExperimentPlan
import Runner
import os, shutil, sys, traceback, time

def PlatformInitialize():
	Context.Runner = Runner.DefaultRunner()
	if os.name == "posix":
		pass
	elif os.name == "nt":
		print "WARNING: Win32 support is experimental."
		import signal
		signal.signal(signal.SIGBREAK, signal.default_int_handler)
	else:
		print "Unsupported system %s" % os.name
		raise ValueError

def LoadChain(filename):
	spec = {}
	execfile(filename, globals(), spec)
	chain = None
	if spec["Type"] == "MultiLevel":
		chain = MultiLevelChain(spec)
	else:
		raise ValueError
	return chain

def LoadCase(filename):
	case = {}
	execfile(filename, globals(), case)
	return case

def LoadMethod(config):

	if config["Method"] == "DOE":
		return MethodDOE(config)
	if config["Method"] == "AdaptiveDOE":
		return MethodAdaptiveDOE(config)
	elif config["Method"] == "Optimization":
		return MethodOpti(config)
	else:
		raise ValueError

def Initialize(case, chain):

	Context.Launcher = ExperimentLauncher(case["Dispatcher"]["Pipelines"])

	Context.Name = case["Name"]
	Context.SimulationChain = chain
	Context.Database = ExperimentPlan(chain)
	Context.ProjectDir = os.path.abspath(os.curdir)

	if case.has_key("ExperimentDirPattern"):
		Context.ExperimentDirPattern = case["ExperimentDirPattern"]

	Context.Launcher.Start()

def Finalize():
	Context.Launcher.PostQuit()
	Context.Launcher.join()
	#Context.Dispatcher.Quit()
	print "Finished on ", time.asctime()

def Splash():
	print "Started on ", time.asctime()
	print "==============================="
	print " d o u g h"
	print "           --- no free lunch"
	print " SVN Revision $Revision"
	print "==============================="
	print

def Main(caseFileName):

	Splash()
	try:
		PlatformInitialize()

		case = LoadCase(caseFileName)
		chain = LoadChain(case["Chain"])
		Initialize(case, chain)

		Context.Method = LoadMethod(case["Config"])

		Context.Method.Start()
	except:
		name, exc, tb = sys.exc_info()
		print name
		print exc
		traceback.print_tb(tb)
	finally:
		Finalize()

if __name__ == "__main__":
	import sys
	Main(sys.argv[1])

