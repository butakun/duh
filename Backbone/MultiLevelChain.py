# $Id: MultiLevelChain.py 123 2012-09-18 16:42:42Z kato $

from Chain import Chain
import Tasks, Context

class MultiLevelChain(Chain):

	def __init__(self, spec):
		Chain.__init__(self)
		assert(spec["Type"] == "MultiLevel")
		self.ChainSpec = spec["Chain"]
		self.Licenses = spec["Licenses"]
		for lic in self.Licenses:
			lic["Count"] = lic["MaxCount"]
		self.Tasks = {}
		for i, taskSpec in enumerate(spec["Tasks"]):
			if self.FindTaskInChain(taskSpec["Name"]) == None:
				print "MultiLevelChain: Task %s not referenced in the chain, skipping it" % taskSpec["Name"]
				continue
			task = Tasks.Create(self, taskSpec)
			task.ID = i + 1
			self.Tasks[task.Name] = task

		Chain.Initialize(self)

	def NextReadyTask(self, experiment):
		nextTask, priority = None, None
		for level, taskNames in enumerate(self.ChainSpec):
			pri = experiment.ID * 1000 + level
			for taskName in taskNames:
				task = self.Tasks[taskName]
				if experiment.Context["TaskStatus"][taskName] == "READY":
					"""
					if task.License:
						if self.IsLicenseAvailable(task.License):
							nextTask, priority = task, pri
							break
					else:
						nextTask, priority = task, pri
						break
					"""
					nextTask, priority = task, pri
					break
		return nextTask, priority

	def TaskStatusChanged(self, experiment, taskName, status):
		#print "*** MultiLevelChain.TaskStatusChanged: exp %d, task %s, status %s" % (experiment.ID, taskName, status)
		newStatus = experiment.Context["TaskStatus"][taskName]
		if newStatus == "DONE":
			self.__PrepareNextLevel(experiment)
		elif newStatus == "ERROR":
			self.__SkipNextLevels(experiment, taskName)

	def __PrepareNextLevel(self, experiment):
		taskStatus = experiment.Context["TaskStatus"]
		numLevels = len(self.ChainSpec)
		for level in range(numLevels):
			tasks = self.ChainSpec[level]
			thisLevelDone = True
			for task in tasks:
				if taskStatus[task] != "DONE":
					thisLevelDone = False
					break
			if thisLevelDone and level < numLevels - 1:
				for task in self.ChainSpec[level + 1]:
					if taskStatus[task] == "WAITING":
						taskStatus[task] = "READY"
						#print "*** MultiLevelChain: Experiment %d, Task %s is now READY" % (experiment.ID, task)

	def __SkipNextLevels(self, experiment, taskName):
		# Task "taskName" received ERROR, so mark everything downstream as ERROR.
		print "MultiLevelChain::SkipNextLevels: task \"%s\" of Exp %d received ERROR, so we mark downstream tasks as ERROR" % (taskName, experiment.ID)
		taskStatus = experiment.Context["TaskStatus"]
		numLevels = len(self.ChainSpec)
		for level in range(numLevels):
			tasks = self.ChainSpec[level]
			if taskName in tasks:
				for i in range(level + 1, numLevels):
					tasksToSkip = self.ChainSpec[i]
					for task in tasksToSkip:
						taskStatus[task] = "ERROR"
				break

	def InitializeExperiment(self, experiment):
		assert(experiment.ID >= 0)
		try:
			directory = Context.ExperimentDirPattern % experiment.ID
		except:
			directory = Context.ExperimentDirPattern
		experiment.Context["Directory"] = directory
		experiment.Context["TaskStatus"] = {}
		for taskName in self.Tasks:
			experiment.Context["TaskStatus"][taskName] = "WAITING"
		for taskName in self.ChainSpec[0]:
			experiment.Context["TaskStatus"][taskName] = "READY"

	def FindTaskInChain(self, taskName):
		for level in range(len(self.ChainSpec)):
			taskNamesInThisLevel = self.ChainSpec[level]
			if taskName in taskNamesInThisLevel:
				return level
		return None

