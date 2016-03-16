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
# $Id: TaskRunner.py 102 2011-09-22 18:14:06Z kato $

from Looper import Looper
import sys, traceback

class TaskRunner(Looper):

	def __init__(self, launcher, name):
		Looper.__init__(self)
		self.Launcher = launcher
		self.Name = name
		print "TaskRunner %s created" % self.Name

	def MessageReceived(self, msg):

		if msg["what"] == "NEW_TASK":
			task = msg["task"]
			exp = msg["exp"]
			self.TaskReceived(task, exp)
		else:
			Looper.MessageReceived(self, msg)

	def TaskReceived(self, task, exp):

		#print "Runner %s: task received, task %s, exp %d" % (self.Name, task.Name, exp.ID)

		# Run the task
		try:
			task.Start(exp)
		except:
			e = sys.exc_info()
			traceback.print_exception(e[0], e[1], e[2])
			print "TaskRunner %s: exp %d task %s failed" % (self.Name, exp.ID, task.Name)
			exp.MarkTask(task.Name, "ERROR")

		self.Launcher.PostMessage({"what":"TASK_DONE", "task":task, "exp":exp, "who":self})

		#print "Runner %s: task done, task %s, exp %d" % (self.Name, task.Name, exp.ID)

