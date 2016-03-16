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
# $Id: MultiThreadDispatcher.py 44 2010-09-21 15:31:56Z kato $

from Dispatcher import Dispatcher
import threading, Queue, time

def Worker(master, tid):

	while True:
		try:
			job = master.Queue.get(block = True, timeout = 3)
		except Queue.Empty:
			if master.WaitingToQuit:
				break
			job = None
		if job:
			master.Lock.acquire()
			master.Count -= 1
			assert(master.Count >= 0)
			priority, job = job
			print "*** Dispatcher.Worker %d " % tid, job["ID"]
			print >>master.Log, "%s: Dipatcher.Worker %d (%d): starting Job %s" % (time.asctime(), tid, master.Count, job["ID"])
			master.Log.flush()
			master.Lock.release()
			try:
				master.Runner.Run(job)
			except:
				pass
			master.Queue.task_done()
			master.Lock.acquire()
			master.Count += 1
			print >>master.Log, "%s: Dipatcher.Worker %d (%d): finished Job %s" % (time.asctime(), tid, master.Count, job["ID"])
			master.Log.flush()
			master.Lock.release()
	master.Lock.acquire()
	print "*** Dispatcher.Worker %d quitting" % tid
	master.Lock.release()

class MultiThreadDispatcher(Dispatcher):

	def __init__(self, pipelines = 4):

		Dispatcher.__init__(self)
		self.Queue = Queue.PriorityQueue(-1)
		self.WaitingToQuit = False
		self.Workers = []
		self.Lock = threading.Lock()
		self.Count = pipelines	# indicates the number of available workers, used in IsFull()
		self.Log = open("dispatcher.log", "w")
		for i in range(pipelines):
			worker = threading.Thread(target = Worker, args = (self, i + 1))
			worker.start()
			self.Workers.append(worker)

	def Submit(self, job, priority):

		self.Queue.put((priority, job))

	def Quit(self):

		self.WaitingToQuit = True
		self.Queue.join()

	def IsFull(self):

		self.Lock.acquire()
		count = self.Count
		qsize = self.Queue.qsize()
		self.Lock.release()
		return count - qsize <= 0

if __name__ == "__main__":
	dispatcher = MultiThreadDispatcher(pipelines = 4)
	for i in range(7):
		job = {"ID":i, "Directory":".", "Command":"echo %d; sleep 2" % i, "Callback":None}
		dispatcher.Submit(job)
	dispatcher.Quit()

