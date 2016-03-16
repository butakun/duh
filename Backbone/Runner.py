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

