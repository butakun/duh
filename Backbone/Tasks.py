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
# $Id: Tasks.py 104 2011-09-24 16:52:35Z kato $

import shutil, os.path, copy, sys
import Context

def Create(chain, spec):

	taskType = spec["Type"]
	taskName = spec["Name"]
	if taskType == "Parameters":
		return Parameters(chain, spec)
	elif taskType == "ExportParameters":
		return ExportParameters(chain, spec)
	elif taskType == "Execution":
		return Execution(chain, spec)
	elif taskType == "PythonFunction":
		return PythonFunction(chain, spec)
	elif taskType == "ExtractResponses":
		return ExtractResponses(chain, spec)
	elif taskType == "Responses":
		return Responses(chain, spec)
	else:
		print "Unknown task type = ", taskType
		return None

def RowColumnExtract(filePath, row, column):
	lines = open(filePath).read().split(os.linesep)
	line = lines[row - 1]
	cols = line.split()
	return cols[column - 1]

class Task(object):

	def __init__(self, chain, spec):
		self.Chain = chain
		self.ID = -1 # will be assigned by the owner chain
		self.Name = spec["Name"]
		self.Heavy = False
		self.Config = spec["Config"]
		self.License = None
		self.Success = None
		if "License" in spec:
			self.License = spec["License"]
		if "Success" in spec:
			self.Success = spec["Success"]
			for spec in self.Success:
				self.Chain.SuccessFlags.append({"Name":spec["Name"]})

	def Start(self, experiment):
		self.CheckOutLicense()
		try:
			status = self.Run(experiment)
			experiment.MarkTask(self.Name, status)
			self.SuccessCheck(experiment)
		except:
			self.CheckInLicense()
			experiment.MarkTask(self.Name, "ERROR")
			type, value, traceback = sys.exc_info()
			print "Task.Start: ERROR"
			print "  ", type, value, traceback
			raise
		self.CheckInLicense()

	def CheckOutLicense(self):
		if not self.License:
			return
		self.Chain.CheckOutLicense(self.License)

	def CheckInLicense(self):
		if not self.License:
			return
		self.Chain.CheckInLicense(self.License)

	def SuccessCheck(self, experiment):
		if not self.Success:
			return
		for spec in self.Success:
			name = spec["Name"]
			value = None
			if spec["Method"] == "RowColumn":
				value = RowColumnExtract(
					os.path.join(experiment.Context["Directory"], spec["File"]),
					spec["Where"]["Row"], spec["Where"]["Column"]
					)
			elif spec["Method"] == None:
				pass
			else:
				print "Extraction method %s not supported." % spec["Method"]
				raise ValueError
			cri = spec["Criterion"]
			if cri == None:
				pass
			elif cri["Type"] == "Keyword":
				experiment.SuccessFlag(name)["Value"] = value
				experiment.SuccessFlag(name)["Success"] = value == cri["Value"]
			elif cri["Type"] == "LessThan":
				value = float(value)
				experiment.SuccessFlag(name)["Value"] = value
				experiment.SuccessFlag(name)["Success"] = value < cri["Value"]
			elif cri["Type"] == "GreaterThan":
				value = float(value)
				experiment.SuccessFlag(name)["Value"] = value
				experiment.SuccessFlag(name)["Success"] = value > cri["Value"]
			else:
				print "Criterion type %s not supported." % cri["Type"]
				raise ValueError

class Parameters(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)
		self.Chain.Parameters.extend(self.Config)

	def Run(self, experiment):
		return "DONE"

class ExportParameters(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)
		self.Chain.TemplateFiles.append(self.Config["TemplateFile"])
		self.Chain.NeedsDirectory = True

	def Run(self, experiment):
		templateFilePath = os.path.join(Context.ProjectDir, self.Config["TemplateFile"])
		template = open(templateFilePath).read()
		for spec in self.Config["Parameters"]:
			template = self.__Export(template, spec, experiment)

		targetFilePath = os.path.join(experiment.Context["Directory"], self.Config["File"])
		open(targetFilePath, "w").write(template)

		return "DONE"

	def __Export(self, template, spec, experiment):
		value = experiment.Parameter(spec["Name"])["Value"]
		where = spec["Where"]
		if spec["Method"] == "RowColumn":
			buf = self.__RowColumnExport(template, where["Row"], where["Column"], value)
		else:
			raise Error
		return buf

	def __RowColumnExport(self, template, row, column, value):
		#lines = template.split(os.linesep) # this fails if the template is in unix line endings (LF) and this is running on windows where linesep = CRLF.
		lines = template.split('\n')
		line = lines[row - 1]
		cols = line.split()
		cols[column - 1] = "%20.12e" % value
		lines[row - 1] = ' '.join(cols)
		return os.linesep.join(lines)

class Execution(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)
		self.Heavy = True
		self.Chain.NeedsDirectory = True

	def Run(self, experiment):
		job = {
			"ID":"Exp%04d_%s" % (experiment.ID, self.Name),
			"Directory":experiment.Context["Directory"],
			"Command":self.Config,
			"EnvironmentVariables":{"DUH_EXPERIMENT_ID":experiment.ID, "DUH_TASK_NAME":self.Name},
			"Stdout":"%s.stdout" % self.Name,
			"StartedCallback":None,
			"FinishedCallback":None
			}
		experiment.MarkTask(self.Name, "RUNNING")

		status = Context.Runner.Run(job)

		#self.CheckInLicense()
		self.SuccessCheck(experiment)
		experiment.MarkTask(self.Name, status)
		Context.Launcher.PostUpdateRequest()

		return status

class PythonFunction(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)

	def Run(self, experiment):
		func = self.Config
		status = "DONE"
		try:
			func(experiment)
		except:
			status = "ERROR"
			print "Python function threw an exception:", sys.exc_info()
		return status

class ExtractResponses(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)
		self.Chain.NeedsDirectory = True

	def Run(self, experiment):
		filePath = os.path.join(experiment.Context["Directory"], self.Config["File"])
		lines = open(filePath).read().split(os.linesep)
		for spec in self.Config["Responses"]:
			if spec["Method"] == "RowColumn":
				row = spec["Where"]["Row"]
				column = spec["Where"]["Column"]
				line = lines[row - 1]
				cols = line.split()
				value = float(cols[column - 1])
				experiment.Response(spec["Name"])["Value"] = value
			else:
				raise ValueError
		return "DONE"

class Responses(Task):

	def __init__(self, chain, spec):
		Task.__init__(self, chain, spec)
		self.Chain.Responses.extend(self.Config)

	def Run(self, experiment):
		return "DONE"

