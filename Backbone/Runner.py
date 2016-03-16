# $Id: Runner.py 95 2011-04-28 03:41:20Z kato $

import os, os.path
import Context

def DefaultRunner():

	if os.name == "posix":
		return POSIXRunner()
	elif os.name == "nt":
		return Win32Runner()
	else:
		print "Unsupported platform: os.name = %s" % os.name
		raise ValueError

class Runner(object):

	def Run(self, job):
		raise Error

class POSIXRunner(Runner):

	def __init__(self):
		pass

	def Run(self, job):

		if job["StartedCallback"]:
			func, data = job["StartedCallback"]
			func(None, data)

		commandline = "export PROJECT_DIR=%s" % Context.ProjectDir
		for env, val in job["EnvironmentVariables"].items():
			commandline += "; export %s=%s" % (env, val)
		commandline += "; cd %s; %s > %s 2>&1" % (job["Directory"], job["Command"], job["Stdout"])
		#commandline += "; cd %s; %s | tee %s 2>&1" % (job["Directory"], job["Command"], job["Stdout"])
		exit_status = os.system(commandline)
		if exit_status == 0:
			status = "DONE"
		else:
			print "Runner: os.system failed: Dir: %s, Command: %s" % (job["Directory"], job["Command"])
			status = "ERROR"

		if job["FinishedCallback"]:
			func, data = job["FinishedCallback"]
			func(status, data)

		return status

class Win32Runner(Runner):

	def __init__(self):
		pass

	def Run(self, job):

		if job["StartedCallback"]:
			func, data = job["StartedCallback"]
			func(None, data)

		batch = "set PROJECT_DIR=%s\n" % Context.ProjectDir
		for env, val in job["EnvironmentVariables"].items():
			batch += "set %s=%s\n" % (env, val)
		batch += "cd %s\n" % job["Directory"]
		batch += "%s > %s 2>&1\n" % (job["Command"], job["Stdout"])
		batchFile = job["Directory"] + os.path.sep + "__DUH__.bat" # FIXME: will not work for parallel
		open(batchFile, "w").write(batch)
		exit_status = os.system(batchFile)

		if exit_status == 0:
			status = "DONE"
		else:
			status = "ERROR"

		if job["FinishedCallback"]:
			func, data = job["FinishedCallback"]
			func(status, data)

		return status

