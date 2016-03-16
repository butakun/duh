# $Id: ExperimentLauncher.py 94 2011-04-14 08:58:20Z kato $

import Context
from Looper import Looper
from TaskRunner import TaskRunner
import os, shutil
import Queue

class ExperimentLauncher(Looper):

	def __init__(self, numRunners = 1):
		Looper.__init__(self)
		self.ExpQueue = []
		self.TaskQueue = Queue.PriorityQueue()

		self.TaskRunners = []
		self.TaskRunnersReady = Queue.Queue()
		for i in range(numRunners):
			r = TaskRunner(self, "%d" % i)
			r.Start()
			self.TaskRunners.append(r)
			self.TaskRunnersReady.put(r)

	def MessageReceived(self, msg):
		Looper.MessageReceived(self, msg)

		what = msg["what"]
		if what == "NEW_EXPERIMENT":
			exp = msg["experiment"]
			callback = msg["callback"]
			self.ExperimentReceived(exp, callback)
		elif what == "UPDATE_EXPERIMENTS":
			self.QueueTasks()
			#self.RunTasks()
		elif what == "TASK_DONE":
			task = msg["task"]
			exp = msg["exp"]
			runner = msg["who"]
			self.TaskDone(task, exp, runner)
		else:
			Looper.MessageReceived(self, msg)

	def PostExperiment(self, exp, callback):
		self.PostMessage({"what":"NEW_EXPERIMENT", "experiment":exp, "callback":callback})

	def PostUpdateRequest(self):
		""" Tasks.Execution calls this method to notify of the completion of an asynchronous execution task. """
		#print "ExperimentLauncher: PostUpdateRequest"
		self.PostMessage({"what":"UPDATE_EXPERIMENTS"})

	def ExperimentReceived(self, exp, callback):

		self.ExpQueue.append([exp, callback])
		#print "ExperimentLauncher: experiment %d queued" % exp.ID
		self.QueueTasks()
		#print "ExperimentLauncher: experiment %d tasks queued" % exp.ID
		#self.RunTasks()

	def QueueTasks(self):

		#print "*** ExpQueue ***"
		#for exp, callback in self.ExpQueue:
		#	print "  Exp %d: %s" % (exp.ID, exp.Status)

		for exp, callback in self.ExpQueue:
			if exp.Status == "READY":
				self.InitializeExperimentDirectory(exp)
				exp.Status = "RUNNING"

			while True:
				#print "ExperimentLauncher: new task from exp %d (%d)? TaskStatus = " % (exp.ID, id(exp)), exp.Context["TaskStatus"]
				task, priority = Context.SimulationChain.NextReadyTask(exp)
				if not task:
					break
				#print "ExperimentLauncher: next ready task of Exp %d = %s" % (exp.ID, task.Name)
				self.TaskQueue.put((priority, (exp, task)))
				exp.MarkTask(task.Name, "QUEUED")
				#print "ExperimentLauncher: task %s of experiment %d queued" % (task.Name, exp.ID)

		# Run tasks
		numRunners = self.TaskRunnersReady.qsize()
		if numRunners == 0:
			# no TaskRunner available to run queued tasks
			return
		numTasks = self.TaskQueue.qsize()
		if numTasks == 0:
			# no task to run
			return

		for i in range(min(numRunners, numTasks)):
			runner = self.TaskRunnersReady.get()
			priority, exp_task = self.TaskQueue.get()
			exp, task = exp_task
			#print "ExperimentLauncher: assigning task %s of exp %d to runner %s" % (task.Name, exp.ID, runner.Name)
			runner.PostMessage({"what":"NEW_TASK", "task":task, "exp":exp})

	def TaskDone(self, task, exp, runner):

		print "ExperimentLauncher: *** TaskDone *** task %s, exp %d, runner %s" % (task.Name, exp.ID, runner.Name)
		self.TaskRunnersReady.put(runner)
		self.RemoveCompletedExperimentsFromQueue()
		self.QueueTasks()

	def RemoveCompletedExperimentsFromQueue(self):

		# Check for experiments that are completed.
		expsDone = []
		for expCallback in self.ExpQueue:
			exp, callback = expCallback
			if exp.IsDoneOrError():
				expsDone.append(expCallback)

		# Remove those completed experiments from the queue.
		for expCallback in expsDone:
			exp, callback = expCallback
			#self.DumpExpQueue()
			#print "ExperimentLauncher: removing Exp %d(%d), index = %d: " % (exp.ID, id(exp), self.ExpQueue.index(expCallback)), exp
			self.ExpQueue.remove(expCallback)
			#self.DumpExpQueue()
			if callback:
				func, data = callback
				#print "ExperimentLauncher: sending callback for Exp %d w/ data = " % exp.ID, data
				func(data)

	def DumpExpQueue(self):
		print "ExpQueue = ", [ (e.ID, id(e)) for e, c in self.ExpQueue ]

	def InitializeExperimentDirectory(self, exp):

		#print "ExperimentLauncher: initializing Exp %d(%d)" % (exp.ID, id(exp))
		Context.SimulationChain.InitializeExperiment(exp)
		if not Context.SimulationChain.NeedsDirectory:
			return

		expDir = exp.Context["Directory"]
		if os.path.exists(expDir):
			if os.path.isdir(expDir):
				print "Warning: experiment directory already exists: %s" % expDir
			else:
				print "Error: non-directory entity exists, preventing experiment directory: %s" % expDir
				raise IOError
		else:
			os.mkdir(expDir)
		for filename in Context.SimulationChain.TemplateFiles:
			src = os.path.join(Context.ProjectDir, filename)
			shutil.copy(src, expDir)

	def QuitRequested(self):

		for runner in self.TaskRunners:
			runner.PostQuit()
			runner.join()

