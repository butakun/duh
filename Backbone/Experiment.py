# $Id: Experiment.py 130 2013-10-29 01:15:50Z kato $

import copy, threading
import numpy as n

class Experiment(dict):

	"""
	Parameter = {"Name":name, "Type":"FLOAT", "Value":val, "Ref":ref, "Min":min, "Max":max }
	Response = {"Name":name, "Type":"FLOAT", "Value":val }
	"""

	def __init__(self, expID, chain):
		self.Chain = chain
		self.ID = expID
		self.Status = "READY"
		self.Parameters = copy.deepcopy(chain.Parameters)
		self.Responses = copy.deepcopy(chain.Responses)
		self.SuccessFlags = copy.deepcopy(chain.SuccessFlags)
		self.Context = {}
		self.Lock = threading.RLock()
		for param in self.Parameters:
			param["Value"] = param["Ref"]
		for resp in self.Responses:
			resp["Value"] = 0.0
		for success in self.SuccessFlags:
			success["Success"] = False

	def Parameter(self, name):
		return filter(lambda v: v["Name"] == name, self.Parameters)[0]

	def Response(self, name):
		return filter(lambda v: v["Name"] == name, self.Responses)[0]

	def Value(self, name):
		v = filter(lambda v: v["Name"] == name, self.Parameters)
		if not v:
			v = filter(lambda v: v["Name"] == name, self.Responses)
		assert(len(v) == 1)
		return v[0]

	def SuccessFlag(self, name):
		return filter(lambda v: v["Name"] == name, self.SuccessFlags)[0]

	def ParametersAsVector(self):
		return n.array(map(lambda v: v["Value"], self.Parameters))

	def ResponsesAsVector(self):
		return n.array(map(lambda v: v["Value"], self.Responses))

	def SuccessFlagsAsVector(self):
		return n.array(map(lambda v: v["Success"], self.SuccessFlags))

	def SetParameters(self, param):
		""" Set parameters to the vector given by "param" """
		for i, v in enumerate(param):
			self.Parameters[i]["Value"] = v

	def IsSuccess(self):
		return self.Status == "DONE" and all(self.SuccessFlagsAsVector())

	def HasMoreTasksToRun(self):
		if "ERROR" in self.Context["TaskStatus"].values():
			return False
		else:
			waiting = "WAITING" in self.Context["TaskStatus"].values()
			ready = "READY" in self.Context["TaskStatus"].values()
			return waiting or ready

	def IsDoneOrError(self):
		return self.Status == "DONE" or self.Status == "ERROR" or self.Status == "SKIP"

	def MarkTask(self, taskname, status):
		self.Lock.acquire()
		self.Context["TaskStatus"][taskname] = status
		self.Chain.TaskStatusChanged(self, taskname, status)
		self.UpdateStatus()
		#print "Experiment: Exp %d Marking Task %s %s" % (self.ID, taskname, status)
		self.Lock.release()

	def UpdateStatus(self):
		# Marks self.Status according to self.Context["TaskStatus"]
		self.Lock.acquire()
		statusValues = self.Context["TaskStatus"].values()
		# FIXME: re-think this logic...
		if "QUEUED" in statusValues or "RUNNING" in statusValues:
			self.Status = "RUNNING"
		elif "READY" in statusValues:
			if self.Status != "RUNNING":
				self.Status = "READY"
		elif "WAITING" in statusValues:
			if self.Status != "RUNNING":
				self.Status = "READY"
		elif all(map(lambda v: v == "DONE", statusValues)):
			self.Status = "DONE"
		elif all(map(lambda v: v == "DONE" or v == "ERROR", statusValues)):
			self.Status = "ERROR"
		else:
			self.Lock.release()
			print "Unknown status = ", self.Context
			raise Exception
		self.Lock.release()

	def __repr__(self):
		return "ID:%d, Status:%s," % (self.ID, self.Status) + str(self.Parameters) + ", " + str(self.Responses) + ", " + str(self.SuccessFlags) + ", " + str(self.Context)

	def __eq__(self, e):
		return self.ID == e.ID

