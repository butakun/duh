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
# $Id: Chain.py 129 2013-10-08 08:45:03Z kato $

import threading
import Logger
import numpy as np

class Chain(object):

	def __init__(self):
		self.Parameters = []
		self.Responses = []
		self.SuccessFlags = []
		self.TemplateFiles = []
		self.Licenses = []
		self.NeedsDirectory = False
		self.Lock = threading.Lock()
		self.Sems = {}

	def Initialize(self):
		for l in self.Licenses:
			self.Sems[l["Name"]] = threading.Semaphore(l["MaxCount"])
			Logger.Out("Created semaphore %s %d" % (l["Name"], l["MaxCount"]))

	def NextTask(self, experiment):
		raise Exception

	def TaskStatusChanged(self, experiment, taskName, status):
		raise Exception

	def InitializeExperiment(self, experiment):
		raise Exception

	def License(self, name):
		return filter(lambda v: v["Name"] == name, self.Licenses)[0]

	"""
	def IsLicenseAvailable(self, name):
		self.Lock.acquire()
		r = self.License(name)["Count"] > 0
		self.Lock.release()
		return r
	"""

	def CheckOutLicense(self, name):
		"""
		self.Lock.acquire()
		self.License(name)["Count"] -= 1
		print "CHECKOUT ", name, self.Licenses
		assert(self.License(name)["Count"] >= 0)
		self.Lock.release()
		"""
		Logger.Out("acquiring %s" % name)
		sem = self.Sems[name]
		sem.acquire()
		Logger.Out("CHECKOUT %s %s" % (name, str(self.Licenses)))

	def CheckInLicense(self, name):
		"""
		self.Lock.acquire()
		self.License(name)["Count"] += 1
		print "CHECKIN ", name, self.Licenses
		assert(self.License(name)["Count"] <= self.License(name)["MaxCount"])
		self.Lock.release()
		"""
		Logger.Out("releasing %s" % name)
		sem = self.Sems[name]
		sem.release()
		Logger.Out("CHECKIN %s %s" % (name, str(self.Licenses)))

	def ParameterSpecsAsVectors(self):
		"""
		returns [paramMin, paramMax, paramRef], each of which is a numpy vector
		"""
		numParams = len(self.Parameters)
		paramMin, paramMax, paramRef = np.zeros(numParams), np.zeros(numParams), np.zeros(numParams)

		for i in range(numParams):
			paramMin[i] = self.Parameters[i]["Min"]
			paramMax[i] = self.Parameters[i]["Max"]
			paramRef[i] = self.Parameters[i]["Ref"]

		return paramMin, paramMax, paramRef

